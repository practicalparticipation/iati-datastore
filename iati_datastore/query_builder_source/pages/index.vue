<template>
  <div>
    <b-container class="bg-dark ml-0 mr-0" fluid>
      <b-jumbotron
        header="IATI Datastore Classic"
        lead="The classic version of the IATI Datastore, reloaded."
        class="mb-0 mt-0 text-center"
        bg-variant="dark"
        text-variant="light"
        >
        <b-container>
          <template v-if="busy">
            <b-spinner label="Checking health..." variant="secondary"></b-spinner>
            <br />
            <p class="text-center">Checking Datastore status...</p>
          </template>
          <template v-else>
            <p class="lead">
              Access <code>{{ formatNumber(healthData.indexed_activities) }}</code> activities and <code>{{ formatNumber(healthData.indexed_transactions) }}</code> transactions.
            </p>
            <hr />
            <h5>
              <b-row>
                <b-col class="bg-success p-2" v-if="healthData.ok == true" md="6">
                  Datastore fully operational
                </b-col>
                <b-col class="bg-danger p-2" v-else md="6">
                    Datastore has some problems
                </b-col>
                <b-col class="bg-secondary p-2" md="6">
                  Last updated: {{ healthData.status_data.last_parsed }}
                </b-col>
              </b-row>
            </h5>
          </template>
          <hr />
          <b-row>
            <b-col>
              <b-btn :href="`${baseURL}/docs/`" variant="primary">View documentation</b-btn>
              <b-btn :href="`${baseURL}/api/`" variant="warning">View API</b-btn>
            </b-col>
          </b-row>
        </b-container>
      </b-jumbotron>
    </b-container>
    <b-container class="bg-light p-4">
      <b-row>
        <b-col>
          <h1>
            <a id="get-the-data" href="#get-the-data">Get the data</a>
          </h1>
          <p>You can obtain data from IATI Datastore Classic in various formats.</p>
          <p>You can choose to filter based on which organisation is reporting the information, where the activity is happening, and the activity's sector. You can choose to output individual activities, transactions or budgets.</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <h2>Choose your filters</h2>
          <p>These options let you filter IATI data, depending on what you are looking for. Additional filters <a :href="`${baseURL}/docs/api/#filtering`">are available</a> by querying the datastore directly.</p>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card
          header="Specific activities"
          header-tag="h4"
          class="mb-3">
            <b-card-text>
              Search for specific activities using the IATI Identifier, Title or Description.
            </b-card-text>
            <b-row>
              <b-col>
                <b-form-group
                  label="IATI Identifier"
                  description="Search for an activity containing a specific IATI Identifier (similar to a project code).">
                  <b-input
                    v-model="filters['iati-identifier']"
                    placeholder="All IATI Identifiers">
                  </b-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group
                  label="Title"
                  description="Search for activities with titles containing the specified text.">
                  <b-input
                    v-model="filters.title"
                    placeholder="All titles">
                  </b-input>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                  label="Description"
                  description="Search for activities with descriptions containing the specified text.">
                  <b-input
                    v-model="filters.description"
                    placeholder="All descriptions">
                  </b-input>
                </b-form-group>
              </b-col>
            </b-row>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-card
            header="Reporting Organisation"
            header-tag="h4"
            class="mb-3">
            <b-card-text>
              The reporting organisation is the publisher of the IATI data.
            </b-card-text>
            <b-row>
              <b-col>
                <b-form-group
                  label="Reporting Organisation Type"
                  description="All types of publishers (e.g. Governments).">
                  <v-select
                    v-model="filters['reporting-org.type']"
                    :options="codelists['OrganisationType']"
                    placeholder="All types of reporting organisation"
                    :reduce="item => item.code"
                    multiple>
                  </v-select>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                  label="Reporting Organisation"
                  description="Select only a particular publisher's data (e.g. DFID).">
                  <v-select
                    v-model="filters['reporting-org']"
                    :options="filteredReportingOrganisations"
                    placeholder="All reporting organisations"
                    :reduce="item => item.code"
                    multiple>

                  </v-select>
                </b-form-group>
              </b-col>
            </b-row>
          </b-card>
          <b-card
            header="Sector"
            header-tag="h4"
            class="mb-3">
            <b-form-group
              label="Sector"
              description="Choose the sector or sectors you are looking for.">
              <v-select
                v-model="filters['sector']"
                :options="codelists['Sector']"
                placeholder="All sectors"
                :reduce="item => item.code"
                multiple></v-select>
            </b-form-group>
            <b-alert variant="info" show>
              For more details of the sectors, see the <a href="https://codelists.codeforiati.org/Sector" rel="noopener noreferrer" target="_blank">DAC 5 Digit Sector</a> codelist.
            </b-alert>
          </b-card>
          <b-card
            header="Recipient location"
            header-tag="h4"
            class="mb-3">
            <b-row>
              <b-col>
                <b-form-group
                label="Recipient country">
                  <v-select
                    v-model="filters['recipient-country']"
                    :options="codelists['Country']"
                    placeholder="All recipient countries"
                    :reduce="item => item.code"
                    multiple>
                  </v-select>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                label="Recipient region">
                  <v-select
                    v-model="filters['recipient-region']"
                    :options="codelists['Region']"
                    placeholder="All recipient regions"
                    :reduce="item => item.code"
                    multiple>
                  </v-select>
                </b-form-group>
              </b-col>
            </b-row>
            <b-alert
              variant="warning"
              :show="(filters['recipient-country'].length > 0) && (filters['recipient-region'].length > 0)">
              Choosing a region and a country will likely not return data, as most publishers publish either a country or a region.
            </b-alert>
          </b-card>
          <b-card
            header="Dates"
            header-tag="h4"
            class="mb-3">
            <b-row>
              <b-col>
                <b-form-group
                label="Start date (after)">
                  <b-form-datepicker
                    v-model="filters['start-date__gt']">
                  </b-form-datepicker>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                label="Start date (before)">
                  <b-form-datepicker
                    v-model="filters['start-date__lt']">
                  </b-form-datepicker>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group
                label="End date (after)">
                  <b-form-datepicker
                    v-model="filters['end-date__gt']">
                  </b-form-datepicker>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group
                label="End date (before)">
                  <b-form-datepicker
                    v-model="filters['end-date__lt']">
                  </b-form-datepicker>
                </b-form-group>
              </b-col>
            </b-row>
          </b-card>
          <h3>How would you like to view this information?</h3>
          <p>These options allow you to configure the way in which your data is disaggregated, making different sorts of analysis possible.</p>
          <b-row>
            <b-col md="4">
              <b-form-group
                label="Choose format">
                <b-radio-group
                  stacked
                  v-model="format"
                  :options="formatOptions">
                </b-radio-group>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <b-form-group
                label="Repeat rows">
                <b-radio-group
                  stacked
                  v-model="grouping"
                  :options="groupingOptions">
                </b-radio-group>
              </b-form-group>
            </b-col>
            <b-col md="4">
              <b-form-group
                label="Choose sample size">
                <b-radio-group
                  stacked
                  v-model="stream"
                  :options="streamOptions">
                </b-radio-group>
              </b-form-group>
            </b-col>
          </b-row>
          <hr />
          <b-row class="mb-2">
            <b-col>
              <b-btn variant="primary" value="Download" :href="queryLink">Download</b-btn>
              <b-btn variant="secondary" value="Reset" @click="reset">Reset</b-btn>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-alert variant="success" show>
                <strong>Your link:</strong>
                <b-input-group>
                  <b-input
                    readonly
                    :value="queryLink"
                    id="query-link">
                  </b-input>
                  <b-input-group-append>
                    <b-btn
                      variant="secondary"
                      @click="copyLink"
                      id="query-link-copy">Copy</b-btn>
                  </b-input-group-append>
                </b-input-group>
                <b-tooltip
                  disabled
                  ref="tooltip"
                  id="query-link-copy-tooltip"
                  target="query-link-copy">
                  Copied!
                </b-tooltip>
              </b-alert>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>

import axios from 'axios'
export default {
  data() {
    return {
      busy: true,
      healthData: {
        "indexed_activities": 0,
        "indexed_transactions": 0,
        "ok": null,
        "status": null,
        "status_data": {
          "last_fetch": null,
          "last_parsed": null,
          "last_successful_fetch": null
        }
      },
      filters: {
        'iati-identifier': null,
        'title': null,
        'description': null,
        'reporting-org': [],
        'reporting-org.type': [],
        'recipient-country': [],
        'recipient-region': [],
        'sector': [],
        'start-date__lt': null,
        'start-date__gt': null,
        'end-date__lt': null,
        'end-date__gt': null
      },
      codelists: {
        'Country': [],
        'Region': [],
        'Sector': [],
        'OrganisationType': [],
        'ReportingOrg': []
      },
      format: 'activity',
      formatOptions: [
        {
          'value': 'activity',
          'text': 'One activity per row',
          'description': "Each row contains a unique activity. Financial information is aggregated. Budget information is excluded. Other potentially repeating fields (such as sectors) are reported in a single cell, delimited by semi-colons."
        },
        {
          'value': 'transaction',
          'text': 'One transaction per row',
          'description': "Each row contains a unique financial transaction. The parent activity identifier and other activity-level fields are repeated for each transaction.<br/>If you are looking to analyse activity finances by year you need to select “Transactions” and calculate the year from the transaction date."
        },
        {
          'value': 'budget',
          'text': 'One budget per row',
          'description': "Each row contains a budget-period entry. Transaction data is not included. The parent activity identifier and other activity-level fields are repeated for each budget line."
        }
      ],
      grouping: '',
      groupingOptions: [
        {
          'value': '',
          'text': 'No',
          'description': "Information is not disaggregated."
        },
        {
          'value': '/by_sector',
          'text': 'Multi-sector expansion',
          'description': "Each Activity, Transaction or Budget row is repeated for each separate Sector reported. The corresponding percentage for the sector split is reported in a separate column. This allows you to easily add arithmetic to your spreadsheet to calculate values proportionately."
        },
        {
          'value': '/by_country',
          'text': 'Multi-country expansion',
          'description': "Each Activity, Transaction or Budget row is repeated for each separate Country reported. The corresponding percentage for the sector split is reported in a separate column. This allows you to easily add arithmetic to your spreadsheet to calculate values proportionately."
        }
      ],
      stream: false,
      streamOptions: [
        {
          'value': false,
          'text': '50 rows',
          'description': "Preview your selection by viewing only the first 50 rows of data."
        },
        {
          'value': true,
          'text': 'Entire selection',
          'description': "Get all results that match your search criteria."
        }
      ],
      codelistURLs: ['Country', 'Region', 'Sector', 'OrganisationType']
    }
  },
  components: {
  },
  computed: {
    baseURL() {
      return this.$axios.defaults.baseURL
    },
    apiURL() {
      return `${this.baseURL}/api/1/access/`
    },
    urlQuery() {
      var _query = {...this.urlQueryFilters}
      if ((this.grouping) && (this.grouping != '')) {
        _query.grouping = this.grouping
      }
      if ((this.stream) && (this.stream == true)) {
        _query.stream = this.stream
      }
      if ((this.format) && (this.format != 'activity')) {
        _query.format = this.format
      }
      return _query
    },
    urlQueryFilters() {
      var _query = {}
      Object.entries(this.filters).forEach(item => {
        if ((item[1]!=null) && (item[1].length > 0)) {
          if ((typeof(item[1])=='object') && (item[1] != null)) {
            _query[item[0]] = item[1].join("|")
          } else {
            _query[item[0]] = item[1]
          }
        }
      })
      return _query
    },
    filteredReportingOrganisations() {
      if (this.filters['reporting-org.type'].length == 0) {
        return this.codelists.ReportingOrg
      }
      return this.codelists.ReportingOrg.filter(org => {
        return this.filters['reporting-org.type'].includes(org.type)
      })
    },
    queryLink() {
      var _urlQueryFilters = Object.entries(this.urlQueryFilters)
      if (this.stream === true) {
        _urlQueryFilters.push(['stream', 'True'])
      }
      const _params = _urlQueryFilters.map(item => {
        return `${item[0]}=${item[1]}`
      }).join("&")
      const params = _params.length > 0 ? `?${_params}` : ''
      return `${this.apiURL}${this.format}${this.grouping}.csv${params}`
    }
  },
  methods: {
    copyLink() {
      navigator.clipboard.writeText(this.queryLink)
      this.$root.$emit('bv::show::tooltip', 'query-link-copy-tooltip')
      const hideTooltip = () => {
        this.$root.$emit('bv::hide::tooltip', 'query-link-copy-tooltip')
      }
      setTimeout(hideTooltip, 1000)
    },
    formatNumber(number) {
      return parseFloat(number).toLocaleString()
    },
    reset() {
      this.filters = {}
    },
    async loadHealthData() {
      await this.$axios.get(`api/1/about/`)
        .then(response => {
          this.healthData = response.data
        })
        .catch(response => {
          this.healthData.ok = false
          this.healthData.status_data.last_parsed = "unknown"
        }
        )
      this.busy = false
    },
    async loadData() {
      this.codelistURLs.forEach(codelist => {
        axios.get(`https://codelists.codeforiati.org/api/json/en/${codelist}.json`)
        .then(response => {
          this.codelists[codelist] = response.data.data.map(item => {
            return {
              code: item.code,
              label: `${item.code} - ${item.name}`
            }
          })
        })
      })
      axios.get(`https://codelists.codeforiati.org/api/json/en/ReportingOrganisation.json`)
      .then(response => {
        this.codelists['ReportingOrg'] = response.data.data.map(publisher => {
          return {
            code: publisher.code,
            label: `${publisher.code} - ${publisher.name}`,
            type: publisher['codeforiati:organisation-type-code']
          }
        })
      })
    },
    updateParams() {
      this.$router.push({query: this.urlQuery})
    },
    setupFilters() {
      Object.keys(this.$route.query).forEach(item => {
        if (item in this.filters) {
          if ((typeof(this.filters[item])=='object') && (this.filters[item] != null)) {
            this.filters[item] = this.$route.query[item].split("|")
          } else {
            this.filters[item] = this.$route.query[item]
          }
        } else {
          if (item == 'grouping') {
            this.grouping = this.$route.query[item]
          } else if (item == 'stream') {
            this.stream = true
          } else if (item=='format') {
            this.format = this.$route.query[item]
          }
        }
      })
    }
  },
  watch: {
    filters: {
      deep: true,
      handler: function(newFilters) {
        this.updateParams()
      }
    },
    grouping: {
      handler: function(newFilters) {
        this.updateParams()
      }
    },
    stream: {
      handler: function(newFilters) {
        this.updateParams()
      }
    },
    format: {
      handler: function(newFilters) {
        this.updateParams()
      }
    }
  },
  mounted() {
    this.loadHealthData()
    this.loadData()
    this.setupFilters()
  }
}
</script>
