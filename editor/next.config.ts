import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
   output: 'export',  // important for deploying separately if needed
  distDir: 'build',      // default '.next' hota hai, par custom kar sakte
  reactStrictMode: true,
};

export default nextConfig;
