export default {
  codeForIATIProject: 'Un projet de Code for IATI',
  datastoreClassicStrapline: "La version classique de l‘IATI Datastore, renouvelé.",
  access: 'Accédez à',
  activitiesAnd: 'activités et',
  transactions: 'transactions',
  viewDocumentation: 'Voir la documentation (en anglais)',
  viewAPI: "Voir l’API",
  checkingDatastoreStatus: "Vérification des informations sur l’état du Datastore",
  datastoreOperational: 'Le Datastore pleinement opérationnel',
  datastoreProblems: 'Le Datastore a des problèmes',
  lastUpdated: 'Dernière actualisation',
  unknown: 'inconnu',
  getTheData: 'Obtenir les données',
  fields: {
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
      placeholder: 'All sectors'
    }
  }
}