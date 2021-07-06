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
    <b-alert show dismissible fade class="mb-0 text-md-center">
      <b-nav-text>
        Are you using Datastore Classic, including during
        <a href="https://iatistandard.org/en/news/technical-notice-2-iatis-datastore-to-be-integrated-in-new-unified-single-platform/">
        downtime of the official IATI Datastore</a>? We'd
        love to hear from you, so we can better understand our users and their needs.<br />Get in touch with
        us at <a href="mailto:hello@codeforiati.org">hello@codeforiati.org</a>
      </b-nav-text>
    </b-alert>
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
</style>