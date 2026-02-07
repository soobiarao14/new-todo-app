import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  allowedDevOrigins: ["http://192.168.2.107:3000"],
};

export default nextConfig;
