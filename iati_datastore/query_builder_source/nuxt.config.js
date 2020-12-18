const routerBase = process.env.DEPLOY_ENV === 'WITH_SUBFOLDER' ? {
  router: {
    base: '/vuejs-datastore-query-builder/'
  }
} : {}

const axiosBase = process.env.IATI_DATASTORE_DEPLOY_URL ? {
  axios: {
    baseURL: process.env.IATI_DATASTORE_DEPLOY_URL
  }
} : {
  axios: {
  }
}
export default {
  mode: 'spa',
  generate: {
    dir: '../iatilib/frontend/querybuilder/'
  },
  /*
  ** Headers of the page
  */
  head: {
    title: 'IATI Datastore Classic',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'The classic version of the IATI Datastore, reloaded.' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://bootstrap-vue.js.org
    'bootstrap-vue/nuxt',
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    'nuxt-vue-select',
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
    }
  },
  ...routerBase, ...axiosBase
}
