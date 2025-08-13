import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: false,
  // Configure allowed dev origins to silence cross-origin warnings when behind proxies or tunnels
  // https://nextjs.org/docs/app/api-reference/config/next-config-js/allowedDevOrigins
  experimental: {
    allowedDevOrigins: [
      "http://localhost:7500",
      "http://127.0.0.1:7500",
      "http://35.222.235.13:7500",
      "https://35.222.235.13:7500",
    ],
  },
};

export default nextConfig;
