<template>
  <div>
    <b-navbar type="light" variant="light">
      <b-container>
        <b-navbar-brand href="#">
          <a href="https://codeforiati.org">
            <img
              width="100px"
              src="https://codeforiati.org/assets/img/logo.png"
              title="A project of Code for IATI" />
          </a>
        </b-navbar-brand>
        <b-navbar-nav class="ml-auto">
          <b-nav-text>
            <button
              data-c4i-toggle="sidebar"
              type="button"
              aria-controls="c4i-sidebar"
              aria-expanded="false"
              aria-label="Toggle Code for IATI sidebar"
              class="navbar-toggler">
              <span class="navbar-toggler-icon"></span>
            </button>
          </b-nav-text>
        </b-navbar-nav>
      </b-container>
    </b-navbar>
    <nuxt />
    <footer class="bg-light p-4">
      <b-container>
        <b-row>
          <b-col md="6">
            <p><a href="https://github.com/codeforIATI/iati-datastore">IATI Datastore Classic on GitHub</a>, free software licensed under the GNU Affero General Public License v3.</p>
          </b-col>
          <b-col class="text-md-right" md="6">
            IATI Datastore Classic is a project of <a href="https://codeforiati.org">Code for IATI</a>
          </b-col>
        </b-row>
      </b-container>
    </footer>
  </div>
</template>

<style>
body {
  background-color: #ececec;
}
.navbar-expand .navbar-toggler {
  display: inherit;
}
</style>
<script>
export default {
  head: {
    script: [
      {
        src: 'https://codeforiati.org/sidebar/sidebar.min.js'
      }
    ]
  },

};
</script>