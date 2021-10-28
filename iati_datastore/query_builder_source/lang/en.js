export default {
  codeForIATIProject: 'A project of Code for IATI',
  datastoreClassicStrapline: 'The classic version of the IATI Datastore, reloaded.',
  access: 'Access',
  activitiesAnd: 'activities and',
  transactions: 'transactions',
  viewDocumentation: 'View documentation',
  viewAPI: 'View API',
  checkingDatastoreStatus: "Checking Datastore status",
  datastoreOperational: 'Datastore fully operational',
  datastoreProblems: 'Datastore has some problems',
  lastUpdated: 'Last updated',
  unknown: 'unknown',
  getTheData: 'Get the data',
  fields: {
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
        description: 'All types of publishers (e.g. Governments).',
        placeholder: 'All types of publishers (e.g. Governments).'
      },
      ref: {
        label: 'Reporting Organisation',
        description: "Select only a particular publisher's data (e.g. DFID).",
        placeholder: 'All reporting organisations'
      }
    },
    sector: {
      label: 'Sector',
      description: 'Choose the sector or sectors you are looking for.',
      placeholder: 'All sectors'
    }
  }
}