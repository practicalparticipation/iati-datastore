export default {
  codeForIATIProject: 'Un projet de Code for IATI',
  datastoreClassic: {
    heading: 'IATI Datastore Classic',
    strapline: "La version classique de l’IATI Datastore, renouvelé.",
  },
  accessText: 'Accédez à {activities} activités et {transactions} transactions.',
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
  outputFormat: {
    chooseFormat: 'Choose format',
    chooseSampleSize: {
      label: 'Choose sample size',
    },
    csvOptions: {
      label: 'CSV Options',
      csvOnlyNote: 'Options only available for CSV output.',
      chooseBreakdown: {
        label: 'Choose breakdown',
      },
      repeatRows: {
        label: 'Repeat rows',
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
      placeholder: 'All IATI Identifiers'
    },
    title: {
      label: 'Titre',
      description: 'Search for activities with titles containing the specified text.',
      placeholder: 'All titles'
    },
    description: {
      label: 'Description',
      description: 'Search for activities with descriptions containing the specified text.',
      placeholder: 'All descriptions'
    },
    activityStatus: {
      label: "Statut de l’activité",
      description: 'Search for activities with only the specified activity status.',
      placeholder: 'All types of activity status'
    },
    reportingOrganisation: {
      label: 'Organisme déclarante',
      description: 'The reporting organisation is the publisher of the IATI data.',
      type: {
        label: 'Type d’organisme déclarante',
        description: 'All types of publishers (e.g. Governments).',
        placeholder: 'All types of publishers (e.g. Governments).'
      },
      ref: {
        label: 'Organisme déclarante',
        description: "Select only a particular publisher's data (e.g. DFID).",
        placeholder: 'All reporting organisations'
      }
    },
    sector: {
      label: 'Secteur',
      description: 'Choose the sector or sectors you are looking for.',
      placeholder: 'All sectors',
      note: 'For more details of the sectors, see the <a href="https://codelists.codeforiati.org/fr/Sector" rel="noopener noreferrer" target="_blank">DAC 5 Digit Sector</a> codelist.'
    },
    policyMarker: {
      label: 'Marqueur d’objectifs politiques',
      description: 'A policy or theme addressed by the activity, according to OECD DAC CRS policy markers.',
      code: {
        label: 'Marqueur d’objectifs politiques',
        description: '',
        placeholder: 'All policy markers'
      },
      significance: {
        label: 'Degré d’implication politique',
        placeholder: 'All policy significance'
      }
    },
    recipientLocation: {
      label: 'Recipient Location',
      country: {
        label: 'Pays bénéficiaire',
        description: '',
        placeholder: 'All recipient countries'
      },
      region: {
        label: 'Région bénéficiaire',
        placeholder: 'All recipient regions'
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