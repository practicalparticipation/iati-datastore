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
      </b-container>
    </b-navbar>
    <nuxt />
    <footer class="bg-light p-4">
      <b-container>
        <b-row>
          <b-col md="6">
            <p>Based on the original <a href="http://datastore.iatistandard.org/query/">Datastore Query Builder</a>, which is free software licenced under the GNU General Public License.<br/>
            <ul>
              <li><a href="https://github.com/codeforIATI/datastore-query-builder">Datastore Query Builder on GitHub</a></li>
              <li><a href="https://github.com/codeforIATI/IATI-Datastore">IATI Datastore Classic on Github</a></li>
            </ul>
            </p>
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
</style>
