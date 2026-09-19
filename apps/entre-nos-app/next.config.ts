import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Permite que o Hot Reload (HMR) funcione ao acessar pelo Tailscale (http://entre-nos)
  allowedDevOrigins: [
    "entre-nos",
    "entre-nos.tailb01e14.ts.net",
    "localhost:3001",
    "127.0.0.1:3001",
  ],
};

export default nextConfig;
