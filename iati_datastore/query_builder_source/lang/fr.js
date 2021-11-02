export default {
  codeForIATIProject: 'Un projet de Code for IATI',
  datastoreDowntimeNotice: `Are you using Datastore Classic, including during
    <a href="https://iatistandard.org/en/news/technical-notice-2-iatis-datastore-to-be-integrated-in-new-unified-single-platform/">
    downtime of the official IATI Datastore</a>? We'd
    love to hear from you, so we can better understand our users and their needs.<br />Get in touch with
    us at <a href="mailto:hello@codeforiati.org">hello@codeforiati.org</a>`,
  datastoreClassic: {
    heading: 'IATI Datastore Classic',
    strapline: "La version classique de l’IATI Datastore, renouvelé.",
  },
  accessText: 'Accédez à <code>{activities}</code> activités et <code>{transactions}</code> transactions.',
  viewDocumentation: 'Voir la documentation (en anglais)',
  viewAPI: "Voir l’API",
  health: {
    checkingDatastoreStatus: "Vérification des informations sur l’état du Datastore",
    datastoreOperational: 'Le Datastore est pleinement opérationnel',
    datastoreProblems: 'Le Datastore a des problèmes',
    lastUpdated: 'Dernière actualisation :',
    unknown: 'inconnu',
    queueData: `{itemsOnQueue} datasets are queued for update, out of {NumDatasets} total datasets. Go ahead and use the data, or wait a little while for today's updates to become available.`,
    updatePctComplete: `Daily update {parsingComplete}% complete.`,
    timing: {
      hoursAgo: 'il y a une heure | il y a {hours} heures',
      minutesAgo: 'il y a une minute | il y a {minutes} minutes',
      secondsAgo: 'il y a une seconde | il y a {seconds} secondes'
    }
  },
  getTheData: {
    heading: 'Obtenir les données',
    para1: 'Vous pouvez obtenir des données de IATI Datastore Classic dans différents formats.',
    para2: "Vous pouvez choisir de filtrer selon l'organisme déclarante, l'endroit où se déroule l'activité et le secteur de l’activité. Vous pouvez choisir de sortir des activités, des transactions ou des budgets.",
    chooseFilters: {
      heading: 'Choisir vos filtres',
      text: 'These options let you filter IATI data, depending on what you are looking for. Additional filters <a href="{baseURL}/docs/api/#filtering">are available</a> by querying the datastore directly.'
    }
  },
  howToView: {
    heading: 'How would you like to view this information?',
    text: 'These options allow you to configure the way in which your data is disaggregated, making different sorts of analysis possible.'
  },
  downloadData: {
    buttons: {
      download: 'Télécharger',
      reset: 'Réinitialiser',
    },
    yourLink: 'Votre lien :',
    copy: 'Copier',
    copied: 'Copié !'
  },
  footer: {
    sourceCode: '<a href="https://github.com/codeforIATI/iati-datastore">IATI Datastore Classic on GitHub</a>, free software licensed under the GNU Affero General Public License v3.',
    credits: 'IATI Datastore Classic is a project of <a href="https://codeforiati.org">Code for IATI</a>',
    privacyPolicy: 'Politique de confidentialité - en anglais'
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
      label: 'Identifiant de l’IITA',
      description: 'Search for an activity containing a specific IATI Identifier (similar to a project code).',
      placeholder: 'Tous les identifiants de l’IITA'
    },
    title: {
      label: 'Titre',
      description: 'Search for activities with titles containing the specified text.',
      placeholder: 'Tous les titres'
    },
    description: {
      label: 'Description',
      description: 'Search for activities with descriptions containing the specified text.',
      placeholder: 'Toutes les descriptions'
    },
    activityStatus: {
      label: "Statut de l’activité",
      description: 'Search for activities with only the specified activity status.',
      placeholder: 'Tous les types de statut de l’activité'
    },
    reportingOrganisation: {
      label: 'Organisme déclarante',
      description: 'The reporting organisation is the publisher of the IATI data.',
      type: {
        label: 'Type d’organisme déclarante',
        description: 'Tous les types d’organisme déclarante',
        placeholder: 'Tous les types d’organisme déclarante'
      },
      ref: {
        label: 'Organisme déclarante',
        description: "Select only a particular publisher's data (e.g. DFID).",
        placeholder: 'Tous les organismes déclarante'
      }
    },
    sector: {
      label: 'Secteur',
      description: 'Choose the sector or sectors you are looking for.',
      placeholder: 'Tous les secteurs',
      note: 'For more details of the sectors, see the <a href="https://codelists.codeforiati.org/fr/Sector" rel="noopener noreferrer" target="_blank">DAC 5 Digit Sector</a> codelist.'
    },
    policyMarker: {
      label: 'Marqueur d’objectifs politiques',
      description: 'A policy or theme addressed by the activity, according to OECD DAC CRS policy markers.',
      code: {
        label: 'Marqueur d’objectifs politiques',
        description: '',
        placeholder: 'Tous les marqueurs d’objectifs politiques'
      },
      significance: {
        label: 'Degré d’implication politique',
        placeholder: 'Tous les degrés d’implication politique'
      }
    },
    recipientLocation: {
      label: 'Pays ou région bénéficiaire',
      country: {
        label: 'Pays bénéficiaire',
        description: '',
        placeholder: 'Tous les pays beneficiaires'
      },
      region: {
        label: 'Région bénéficiaire',
        placeholder: 'Toutes les régions beneficiaires'
      },
      note: 'Choosing a region and a country will likely not return data, as most publishers publish either a country or a region.'
    },
    dates: {
      label: 'Dates',
      startDateAfter: 'Start date (after)',
      startDateBefore: 'Start date (before)',
      endDateAfter: 'End date (after)',
      endDateBefore: 'End date (before)'
    }
  }
}