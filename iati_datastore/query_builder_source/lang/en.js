export default {
  codeForIATIProject: 'A project of Code for IATI',
  datastoreDowntimeNotice: `Are you using Datastore Classic, including during
    <a href="https://iatistandard.org/en/news/technical-notice-2-iatis-datastore-to-be-integrated-in-new-unified-single-platform/">
    downtime of the official IATI Datastore</a>? We'd
    love to hear from you, so we can better understand our users and their needs.<br />Get in touch with
    us at <a href="mailto:hello@codeforiati.org">hello@codeforiati.org</a>`,
  datastoreClassic: {
    heading: 'IATI Datastore Classic',
    strapline: 'The classic version of the IATI Datastore, reloaded.',
  },
  accessText: 'Access <code>{activities}</code> activities and <code>{transactions}</code> transactions.',
  viewDocumentation: 'Documentation',
  viewAPI: 'API',
  health: {
    checkingDatastoreStatus: "Checking Datastore status",
    datastoreOperational: 'Datastore fully operational',
    datastoreProblems: 'Datastore has some problems',
    lastUpdated: 'Last updated:',
    unknown: 'unknown',
    queueData: `{itemsOnQueue} datasets are queued for update, out of {NumDatasets} total datasets. Go ahead and use the data, or wait a little while for today's updates to become available.`,
    updatePctComplete: `Daily update {parsingComplete}% complete.`,
    timing: {
      hoursAgo: 'one hour ago | {hours} hours ago',
      minutesAgo: 'one minute ago | {minutes} minutes ago',
      secondsAgo: 'one second ago | {seconds} seconds ago'
    }
  },
  getTheData: {
    heading: 'Get the data',
    para1: 'You can obtain data from IATI Datastore Classic in various formats.',
    para2: "You can choose to filter based on which organisation is reporting the information, where the activity is happening, and the activity's sector. You can choose to output individual activities, transactions or budgets.",
    chooseFilters: {
      heading: 'Choose your filters',
      text: 'These options let you filter IATI data, depending on what you are looking for. Additional filters <a href="{baseURL}/docs/api/#filtering">are available</a> by querying the datastore directly.'
    }
  },
  howToView: {
    heading: 'How would you like to view this information?',
    text: 'These options allow you to configure the way in which your data is disaggregated, making different sorts of analysis possible.'
  },
  downloadData: {
    buttons: {
      download: 'Download',
      reset: 'Reset',
    },
    yourLink: 'Your link:',
    copy: 'Copy',
    copied: 'Copied!'
  },
  footer: {
    sourceCode: '<a href="https://github.com/codeforIATI/iati-datastore">IATI Datastore Classic on GitHub</a>, free software licensed under the GNU Affero General Public License v3.',
    credits: 'IATI Datastore Classic is a project of <a href="https://codeforiati.org">Code for IATI</a>',
    privacyPolicy: 'Privacy Policy'
  },
  outputFormat: {
    chooseFormat: 'Choose format',
    chooseSampleSize: {
      label: 'Choose sample size',
      options: [
        {
          'value': '1',
          'text': '1 row',
          'description': "Preview your selection by viewing only the first row of data."
        },
        {
          'value': '50',
          'text': '50 rows',
          'description': "Preview your selection by viewing only the first 50 rows of data."
        },
        {
          'value': 'stream',
          'text': 'Entire selection',
          'description': "Get all results that match your search criteria."
        }
      ]
    },
    csvOptions: {
      label: 'CSV Options',
      csvOnlyNote: 'Options only available for CSV output.',
      chooseBreakdown: {
        label: 'Choose breakdown',
        options: [
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
      },
      repeatRows: {
        label: 'Repeat rows',
        options: [
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
        ]
      }
    }
  },
  fields: {
    specificActivities: {
      label: 'Specific activities',
      description: 'Search for specific activities using the IATI Identifier, Title or Description.'
    },
    iatiIdentifier: {
      label: 'IATI Identifier',
      description: 'Search for an activity containing a specific IATI Identifier (similar to a project code).',
      placeholder: 'All IATI Identifiers'
    },
    title: {
      label: 'Title',
      description: 'Search for activities with titles containing the specified text.',
      placeholder: 'All titles'
    },
    description: {
      label: 'Description',
      description: 'Search for activities with descriptions containing the specified text.',
      placeholder: 'All descriptions'
    },
    activityStatus: {
      label: 'Activity Status',
      description: 'Search for activities with only the specified activity status.',
      placeholder: 'All types of activity status'
    },
    reportingOrganisation: {
      label: 'Reporting Organisation',
      description: 'The reporting organisation is the publisher of the IATI data.',
      type: {
        label: 'Reporting Organisation Type',
        description: 'Select only a particular type of publisher’s data.',
        placeholder: 'All types of publishers (e.g. Governments).'
      },
      ref: {
        label: 'Reporting Organisation',
        description: 'Select only a particular publisher’s data (e.g. World Bank).',
        placeholder: 'All reporting organisations'
      }
    },
    sector: {
      label: 'Sector',
      description: 'Choose the sector or sectors you are looking for.',
      placeholder: 'All sectors',
      note: 'For more details of the sectors, see the <a href="https://codelists.codeforiati.org/Sector" rel="noopener noreferrer" target="_blank">DAC 5 Digit Sector</a> codelist.'
    },
    policyMarker: {
      label: 'Policy Marker',
      description: 'A policy or theme addressed by the activity, according to OECD DAC CRS policy markers.',
      code: {
        label: 'Policy Marker',
        description: '',
        placeholder: 'All policy markers'
      },
      significance: {
        label: 'Policy Significance',
        placeholder: 'All policy significance'
      }
    },
    recipientLocation: {
      label: 'Recipient country or region',
      country: {
        label: 'Recipient country',
        description: '',
        placeholder: 'All recipient countries'
      },
      region: {
        label: 'Recipient region',
        placeholder: 'All recipient regions'
      },
      note: 'Choosing a region and a country will likely not return data, as most publishers publish either a country or a region.'
    },
    dates: {
      label: 'Dates',
      startDateAfter: 'Start date (after)',
      startDateBefore: 'Start date (before)',
      endDateAfter: 'End date (after)',
      endDateBefore: 'End date (before)',
      datePickerLabels: {
        labelPrevDecade: 'Previous decade',
        labelPrevYear: 'Previous year',
        labelPrevMonth: 'Previous month',
        labelCurrentMonth: 'Current month',
        labelNextMonth: 'Next month',
        labelNextYear: 'Next year',
        labelNextDecade: 'Next decade',
        labelToday: 'Today',
        labelSelected: 'Selected date',
        labelNoDateSelected: 'No date selected',
        labelCalendar: 'Calendar',
        labelNav: 'Calendar navigation',
        labelHelp: 'Use cursor keys to navigate calendar dates'
      },
    }
  }
}