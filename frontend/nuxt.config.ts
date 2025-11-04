// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://127.0.0.1:5000/api'
    }
  }
})

