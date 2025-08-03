import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    optimizeDeps: {
        exclude: ["lucide-react"],
    },
    server: {
        port: 5173,
        host: true,
        proxy: {
            "/api": {
                target: "http://localhost:3001",
                changeOrigin: true,
                secure: false,
                rewrite: (path) => path,
                configure: (proxy, _options) => {
                    proxy.on("error", (err, _req, _res) => {
                        console.log("🚨 Proxy error:", err);
                    });
                    proxy.on("proxyReq", (proxyReq, req, _res) => {
                        console.log(
                            "📤 Proxying request:",
                            req.method,
                            req.url,
                            "→",
                            proxyReq.path,
                        );
                    });
                    proxy.on("proxyRes", (proxyRes, req, _res) => {
                        console.log(
                            "📥 Proxy response:",
                            proxyRes.statusCode,
                            req.url,
                        );
                    });
                },
            },
        },
    },
});
