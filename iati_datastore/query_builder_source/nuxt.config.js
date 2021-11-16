const routerBase = process.env.DEPLOY_ENV === 'WITH_SUBFOLDER' ? {
  router: {
    base: '/vuejs-datastore-query-builder/'
  }
} : {
  router: {
    trailingSlash: true
  }
}

const axiosBase = process.env.IATI_DATASTORE_DEPLOY_URL ? {
  axios: {
    baseURL: process.env.IATI_DATASTORE_DEPLOY_URL
  }
} : {
  axios: {
    baseURL: 'http://127.0.0.1:5000'
  }
}
export default {
  target: 'static',
  generate: {
    dir: '../iatilib/frontend/querybuilder/'
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
    '@nuxtjs/i18n',
  ],
  i18n: {
    locales: [
      {
          'code': 'en',
          'file': 'en.json'
      },
      {
          'code': 'fr',
          'file': 'fr.json'
      },
      {
          'code': 'pt',
          'file': 'pt.json'
      }
    ],
    lazy: true,
    langDir: 'lang/',
    defaultLocale: 'en'
  },
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
