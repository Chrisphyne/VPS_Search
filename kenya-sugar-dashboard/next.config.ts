import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: false,
  // Configure allowed dev origins to silence cross-origin warnings when behind proxies or tunnels
  // https://nextjs.org/docs/app/api-reference/config/next-config-js/allowedDevOrigins
  experimental: {
    allowedDevOrigins: [
      "http://localhost:7500",
      "http://127.0.0.1:7500",
      // If you access UI via public IP/host, add it here for dev warning suppression
      "http://35.222.235.13:7500",
      "https://35.222.235.13:7500",
    ],
  },
};

export default nextConfig;
