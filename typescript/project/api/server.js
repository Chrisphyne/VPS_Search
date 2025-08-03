import express from "express";
import cors from "cors";
import { MeiliSearch } from "meilisearch";
import pkg from "pg";
import dotenv from "dotenv";

const { Pool } = pkg;
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(
    cors({
        origin: [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
        ],
        credentials: true,
    }),
);
app.use(express.json());

// Log startup
console.log("🚀 Starting API server...");
console.log("📍 Port:", PORT);
console.log("🔍 Meilisearch Host:", process.env.MEILISEARCH_HOST);
console.log("🗄️ PostgreSQL Host:", process.env.PG_HOST);

// Meilisearch client
let meiliClient;
try {
    meiliClient = new MeiliSearch({
        host: process.env.MEILISEARCH_HOST || "http://localhost:7700",
        apiKey: process.env.MEILISEARCH_API_KEY,
    });
    console.log("✅ Meilisearch client initialized");
} catch (error) {
    console.error(
        "❌ Meilisearch client initialization failed:",
        error.message,
    );
}

// PostgreSQL connection pool
let pool;
try {
    pool = new Pool({
        host: process.env.PG_HOST,
        port: process.env.PG_PORT,
        database: process.env.PG_DB,
        user: process.env.PG_USER,
        password: process.env.PG_PASSWORD,
    });
    console.log("✅ PostgreSQL pool initialized");
} catch (error) {
    console.error("❌ PostgreSQL pool initialization failed:", error.message);
}

// Test database connection
if (pool) {
    pool.connect((err, client, release) => {
        if (err) {
            console.error("❌ Error connecting to PostgreSQL:", err.message);
        } else {
            console.log("✅ Connected to PostgreSQL successfully");
            release();
        }
    });
}

// Basic health check endpoint
app.get("/", (req, res) => {
    res.json({
        status: "API Server is running",
        timestamp: new Date().toISOString(),
        endpoints: ["/api/health", "/api/search", "/api/sub-modules"],
    });
});

// Helper function to build filters
function buildMeilisearchFilters(params) {
    const filters = [];

    // Database filters
    if (
        params.databases &&
        params.databases.length > 0 &&
        !params.databases.includes("ALL")
    ) {
        const dbFilters = [];

        params.databases.forEach((db) => {
            switch (db) {
                case "WATCHLIST DB":
                    dbFilters.push("victim_name IS NOT NULL");
                    break;
                case "STOLEN/LOST ITEMS DB":
                    dbFilters.push(
                        "(stolen_items IS NOT NULL OR electronic_type IS NOT NULL OR document_type IS NOT NULL)",
                    );
                    break;
                case "MISSING PERSONS DB":
                    dbFilters.push('sub_module_name = "Missing Person"');
                    break;
                case "EVIDENCE DB":
                    dbFilters.push(
                        "(narrative IS NOT NULL OR description IS NOT NULL)",
                    );
                    break;
                case "STOLEN VEHICLES DB":
                    dbFilters.push(
                        '(sub_module_name = "Motor Vehicle Theft" OR vehicle_registration IS NOT NULL)',
                    );
                    break;
                case "PRISONER PROPERTY DB":
                    dbFilters.push("stolen_items IS NOT NULL");
                    break;
            }
        });

        if (dbFilters.length > 0) {
            filters.push(`(${dbFilters.join(" OR ")})`);
        }
    }

    // Sub-module filters
    if (params.subModules && params.subModules.length > 0) {
        const subModuleList = params.subModules
            .map((sm) => `"${sm}"`)
            .join(", ");
        filters.push(`sub_module_name IN [${subModuleList}]`);
    }

    // Date range filters
    if (params.startDate && params.endDate) {
        const startTimestamp = Math.floor(
            new Date(params.startDate).getTime() / 1000,
        );
        const endTimestamp = Math.floor(
            new Date(params.endDate).getTime() / 1000,
        );
        filters.push(
            `submissionDate >= ${startTimestamp} AND submissionDate <= ${endTimestamp}`,
        );
    }

    return filters.length > 0 ? filters.join(" AND ") : null;
}

// Search endpoint
app.post("/api/search", async (req, res) => {
    console.log("🔍 Search request received:", req.body);

    try {
        const {
            query,
            startDate,
            endDate,
            databases = [],
            subModules = [],
            page = 1,
            limit = 10,
            useHybrid = false,
            semanticRatio = 0.5,
        } = req.body;

        if (!query || query.trim() === "") {
            return res.status(400).json({ error: "Query is required" });
        }

        if (!meiliClient) {
            throw new Error("Meilisearch client not available");
        }

        const index = meiliClient.index("incidents");
        const offset = (page - 1) * limit;
        const filters = buildMeilisearchFilters({
            databases,
            subModules,
            startDate,
            endDate,
        });

        console.log("Search query:", query);
        console.log("Filters:", filters);

        let searchOptions = {
            limit,
            offset,
            attributesToRetrieve: ["*"],
        };

        if (filters) {
            searchOptions.filter = filters;
        }

        // Use hybrid search if enabled and embedder is configured
        if (useHybrid) {
            searchOptions.hybrid = {
                embedder: "suspect-ollama",
                semanticRatio: semanticRatio,
            };
        }

        const results = await index.search(query, searchOptions);

        // Get total count for pagination
        const totalResults = await index.search(query, {
            filter: filters,
            limit: 1,
            attributesToRetrieve: ["id"],
        });

        console.log(
            "✅ Search completed:",
            results.hits.length,
            "results found",
        );

        res.json({
            hits: results.hits,
            totalHits: totalResults.estimatedTotalHits,
            processingTimeMs: results.processingTimeMs,
            page,
            totalPages: Math.ceil(totalResults.estimatedTotalHits / limit),
        });
    } catch (error) {
        console.error("❌ Search error:", error.message);
        res.status(500).json({
            error: "Search failed",
            details: error.message,
        });
    }
});

// Get sub-modules endpoint
app.get("/api/sub-modules", async (req, res) => {
    console.log("📋 Sub-modules request received");

    try {
        if (!pool) {
            throw new Error("Database connection not available");
        }

        const client = await pool.connect();
        const result = await client.query(
            "SELECT name FROM sub_module ORDER BY name",
        );
        client.release();

        const subModules = result.rows.map((row) => row.name);
        console.log("✅ Sub-modules fetched:", subModules.length, "items");
        res.json(subModules);
    } catch (error) {
        console.error("❌ Error fetching sub-modules:", error.message);
        res.status(500).json({
            error: "Failed to fetch sub-modules",
            details: error.message,
        });
    }
});

// Index management endpoints
app.post("/api/admin/create-index", async (req, res) => {
    console.log("🔧 Create index request received");

    try {
        if (!meiliClient) {
            throw new Error("Meilisearch client not available");
        }

        const indexName = "incidents";

        // Create index
        await meiliClient.createIndex(indexName, { primaryKey: "id" });

        // Configure settings
        const index = meiliClient.index(indexName);
        const task = await index.updateSettings({
            searchableAttributes: [
                "suspect_name",
                "suspect_description",
                "searchable_text",
                "sub_module_name",
                "description",
                "location",
                "victim_name",
                "vehicle_registration",
                "stolen_items",
            ],
            filterableAttributes: [
                "sub_module_name",
                "stolen_items",
                "electronic_type",
                "document_type",
                "vehicle_registration",
                "victim_name",
                "gbv_type",
                "cause_of_death",
                "mental_condition",
                "suspect_presence",
                "submissionDate",
                "suspect_name",
                "suspect_description",
            ],
            typoTolerance: {
                enabled: true,
                minWordSizeForTypos: {
                    oneTypo: 2,
                    twoTypos: 4,
                },
            },
            rankingRules: [
                "words",
                "typo",
                "proximity",
                "attribute",
                "sort",
                "exactness",
            ],
        });

        await meiliClient.waitForTask(task.taskUid);

        console.log("✅ Index created and configured");
        res.json({
            success: true,
            message: "Meilisearch index created and configured successfully.",
        });
    } catch (error) {
        console.error("❌ Error creating index:", error.message);
        res.status(500).json({
            error: "Failed to create index",
            details: error.message,
        });
    }
});

app.post("/api/admin/index-data", async (req, res) => {
    console.log("📊 Index data request received");

    try {
        if (!meiliClient || !pool) {
            throw new Error("Required services not available");
        }

        const indexName = "incidents";
        const index = meiliClient.index(indexName);

        // Fetch data from PostgreSQL
        const client = await pool.connect();
        const result = await client.query(`
      SELECT smd."id", smd."sub_moduleId", smd."submissionDate", smd."formData", smd."location", smd."narrative",
             sm.name as sub_module_name
      FROM sub_module_data smd
      JOIN sub_module sm ON smd."sub_moduleId" = sm.id
      WHERE sm.name IN ('GBV', 'Stolen Lost Item', 'Robbery', 'Rape', 'Motor Vehicle Theft', 'Missing Person',
                       'Homicide', 'Death', 'Cyber Crime', 'Burglary', 'Assault', 'Arson')
    `);
        client.release();

        console.log("📊 Fetched", result.rows.length, "records from database");

        const documents = result.rows.map((row) => {
            const formData = row.formData || {};
            const searchableValues = [];

            // Extract searchable text from form data
            for (const [key, value] of Object.entries(formData)) {
                if (typeof value === "string") {
                    searchableValues.push(value);
                } else if (value !== null) {
                    searchableValues.push(String(value));
                }
            }

            searchableValues.push(
                row.location || "",
                row.narrative || "",
                row.sub_module_name || "",
            );
            const searchableText = searchableValues.filter(Boolean).join(" ");

            const submissionDate = row.submissionDate
                ? Math.floor(new Date(row.submissionDate).getTime() / 1000)
                : null;

            return {
                id: row.id,
                sub_moduleId: row.sub_moduleId,
                sub_module_name: row.sub_module_name,
                submissionDate: submissionDate,
                location: row.location || formData.location,
                narrative: row.narrative,
                description:
                    formData["Give a brief narrative of what happened"] ||
                    formData["A brief narrative of what happened"] ||
                    formData["A brief description of the person"] ||
                    "N/A",
                type_of_property:
                    formData["Type of property"] ||
                    formData["select type of property broken into"],
                victim_name:
                    formData["Name of the casualty"] ||
                    formData["Name of the victim"] ||
                    formData["Name of the deceased"] ||
                    formData["Name"],
                vehicle_make: formData["Make"],
                vehicle_model: formData["Model"],
                vehicle_registration: formData["Registration number"],
                stolen_items: formData["What category of items were stolen"],
                electronic_type: formData["type of electronic"],
                document_type: formData["type of Documents"],
                gbv_type: formData["Type of GBV"],
                cause_of_death: formData["Cause of death"],
                mental_condition: formData["Mental Condition"],
                suspect_presence: formData["Do you have a suspect"],
                suspect_name: formData["Name of the suspect"],
                suspect_description:
                    formData["Description of the suspect"] ||
                    formData["Give details about the suspect"],
                cyber_incident: formData["Select Incident"],
                platform_digital_violence:
                    formData["Platform In Digital or Online Violence"],
                searchable_text: searchableText,
                formData: formData,
            };
        });

        // Index documents in batches
        const batchSize = 1000;
        let totalIndexed = 0;

        for (let i = 0; i < documents.length; i += batchSize) {
            const batch = documents.slice(i, i + batchSize);
            const task = await index.addDocuments(batch);
            await meiliClient.waitForTask(task.taskUid);
            totalIndexed += batch.length;
            console.log(
                "📊 Indexed batch:",
                totalIndexed,
                "/",
                documents.length,
            );
        }

        console.log("✅ Indexing completed:", totalIndexed, "documents");
        res.json({
            success: true,
            message: `Indexed ${totalIndexed} documents successfully.`,
            totalDocuments: totalIndexed,
        });
    } catch (error) {
        console.error("❌ Error indexing data:", error.message);
        res.status(500).json({
            error: "Failed to index data",
            details: error.message,
        });
    }
});

app.get("/api/admin/debug-suspects", async (req, res) => {
    console.log("🐛 Debug suspects request received");

    try {
        if (!meiliClient) {
            throw new Error("Meilisearch client not available");
        }

        const index = meiliClient.index("incidents");
        const results = await index.search("", {
            filter: 'suspect_presence = "Yes" AND (suspect_name IS NOT NULL OR suspect_description IS NOT NULL)',
            limit: 10,
            attributesToRetrieve: [
                "suspect_name",
                "suspect_description",
                "sub_module_name",
                "id",
            ],
        });

        console.log(
            "✅ Debug suspects completed:",
            results.hits.length,
            "results",
        );
        res.json({
            success: true,
            message: `Found ${results.hits.length} documents with suspect information.`,
            samples: results.hits,
        });
    } catch (error) {
        console.error("❌ Error debugging suspects:", error.message);
        res.status(500).json({
            error: "Failed to debug suspects",
            details: error.message,
        });
    }
});

app.get("/api/admin/debug-documents", async (req, res) => {
    console.log("🐛 Debug documents request received");

    try {
        if (!meiliClient) {
            throw new Error("Meilisearch client not available");
        }

        const index = meiliClient.index("incidents");
        const stats = await index.getStats();
        const results = await index.search("", {
            limit: 10,
            attributesToRetrieve: ["*"],
        });

        console.log(
            "✅ Debug documents completed:",
            stats.numberOfDocuments,
            "total documents",
        );
        res.json({
            success: true,
            message: `Index contains ${stats.numberOfDocuments} documents across all sub-modules.`,
            stats: stats,
            samples: results.hits,
        });
    } catch (error) {
        console.error("❌ Error debugging documents:", error.message);
        res.status(500).json({
            error: "Failed to debug documents",
            details: error.message,
        });
    }
});

// Health check endpoint
app.get("/api/health", async (req, res) => {
    console.log("🏥 Health check request received");

    try {
        const health = {
            status: "healthy",
            timestamp: new Date().toISOString(),
            services: {},
        };

        // Check Meilisearch
        try {
            if (meiliClient) {
                const response = await fetch(
                    `${process.env.MEILISEARCH_HOST}/health`,
                );
                health.services.meilisearch = response.ok
                    ? "healthy"
                    : "unhealthy";
            } else {
                health.services.meilisearch = "unavailable";
            }
        } catch (error) {
            health.services.meilisearch = "error: " + error.message;
        }

        // Check PostgreSQL
        try {
            if (pool) {
                const client = await pool.connect();
                await client.query("SELECT 1");
                client.release();
                health.services.postgresql = "healthy";
            } else {
                health.services.postgresql = "unavailable";
            }
        } catch (error) {
            health.services.postgresql = "error: " + error.message;
        }

        console.log("✅ Health check completed:", health);
        res.json(health);
    } catch (error) {
        console.error("❌ Health check failed:", error.message);
        res.status(500).json({
            status: "unhealthy",
            error: error.message,
            timestamp: new Date().toISOString(),
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error("❌ Unhandled error:", err.message);
    res.status(500).json({
        error: "Internal server error",
        details: err.message,
    });
});

// 404 handler
app.use((req, res) => {
    console.log("❓ 404 - Route not found:", req.method, req.path);
    res.status(404).json({
        error: "Route not found",
        path: req.path,
        method: req.method,
    });
});

app.listen(PORT, () => {
    console.log(`🚀 API server running on port ${PORT}`);
    console.log(`📍 Health check: http://localhost:${PORT}/api/health`);
    console.log(`🔍 Search endpoint: http://localhost:${PORT}/api/search`);
});
