/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    images: {
        domains: ['127.0.0.1'],
    },
    webpack: (config, { isServer }) => {
        // Add timeout configuration to help with chunk loading errors
        config.watchOptions = {
            aggregateTimeout: 300,
            poll: 1000,
        }
        return config
    },
}

module.exports = nextConfig