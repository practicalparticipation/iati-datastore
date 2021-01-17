# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Get fabric working for deployment ([#113](https://github.com/codeforIATI/iati-datastore/pull/113))
- Recipient region, country and sector also search transactions by default ([#117](https://github.com/codeforIATI/iati-datastore/pull/117))
- Add /api/ and /api/1/ routes ([#120](https://github.com/codeforIATI/iati-datastore/pull/120))
- Add some tests for the generated documentation ([#123](https://github.com/codeforIATI/iati-datastore/pull/123))
- Add some console tests ([#127](https://github.com/codeforIATI/iati-datastore/pull/127))
- Add a home page, including the query builder and information about health status ([#133](https://github.com/codeforIATI/iati-datastore/pull/133))
- Add a route to turn an API request into a populated query builder ([#140](https://github.com/codeforIATI/iati-datastore/pull/140))
- Add search on title and description ([#168](https://github.com/codeforIATI/iati-datastore/pull/168))
- Add a `Stats` model to keep track of totals ([#188](https://github.com/codeforIATI/iati-datastore/pull/188))
- Auto-deploy `main` branch on Github, via Github Actions ([#189](https://github.com/codeforIATI/iati-datastore/pull/189))
- Add issue templates ([#193](https://github.com/codeforIATI/iati-datastore/pull/193))
- Add XML and JSON options to query builder ([#195](https://github.com/codeforIATI/iati-datastore/pull/195))
- Add `iati reset-stats` command ([#199](https://github.com/codeforIATI/iati-datastore/pull/199))
- Add prettier error pages ([#203](https://github.com/codeforIATI/iati-datastore/pull/203))
- Add a changelog ([#222](https://github.com/codeforIATI/iati-datastore/pull/222))

### Changed
- Change xmlns in XML output to https://datastore.codeforiati.org/ns ([#111](https://github.com/codeforIATI/iati-datastore/pull/111))
- Use Flask Migrate for migrations ([#116](https://github.com/codeforIATI/iati-datastore/pull/116))
- Switch to using iatikit to download data much faster and more reliably ([#131](https://github.com/codeforIATI/iati-datastore/pull/131))
- Change default branch from `master` to `main` ([#143](https://github.com/codeforIATI/iati-datastore/pull/143))
- Compare existing hash of data with new data, in order to massively speed up import ([#157](https://github.com/codeforIATI/iati-datastore/pull/157))
- Switch from TravisCI to Github Actions ([#161](https://github.com/codeforIATI/iati-datastore/pull/161))
- Use CodeforIATI codelists for Reporting Org ([#178](https://github.com/codeforIATI/iati-datastore/pull/178))
- Paginate /api/1/about/deleted/ ([#200](https://github.com/codeforIATI/iati-datastore/pull/200))

### Removed
- Remove the `iati create-database` command (use `iati db upgrade` instead) ([#129](https://github.com/codeforIATI/iati-datastore/pull/129))

### Fixed
- Fix a hierachy bug ([#114](https://github.com/codeforIATI/iati-datastore/pull/114))
- Fix a bug for searching on `recipient-region.text` ([#117](https://github.com/codeforIATI/iati-datastore/pull/117))
- Fix some documentation warnings ([#124](https://github.com/codeforIATI/iati-datastore/pull/124))
- Rationalise `_open_resource` ([#156](https://github.com/codeforIATI/iati-datastore/pull/156))
- Fix integrity constraint error with deleted activities ([#164](https://github.com/codeforIATI/iati-datastore/pull/164))
- Fix `stream=True` for CSV and JSON ([#179](https://github.com/codeforIATI/iati-datastore/pull/179))
- Ensure last_parse_error gets saved ([#201](https://github.com/codeforIATI/iati-datastore/pull/201))
- Fix a bug with /api/1/error/dataset.log, and ensure it uses mimetype `text/plain` ([#210](https://github.com/codeforIATI/iati-datastore/pull/210))
- Fix application context bug ([#217](https://github.com/codeforIATI/iati-datastore/pull/217))

## [1.0.0b1] - 2020-12-10

### Added
- Provide prettier documentation ([#97](https://github.com/codeforIATI/iati-datastore/pull/97); ([#99](https://github.com/codeforIATI/iati-datastore/pull/99)) ([#102](https://github.com/codeforIATI/iati-datastore/pull/102)))
- Add a status API page (/api/1/about/) that provides an accurate indication of status ([#101](https://github.com/codeforIATI/iati-datastore/pull/101))
- Add /meta/filters/ API route ([#105](https://github.com/codeforIATI/iati-datastore/pull/105))
- Add trailing slashes to all routes ([#106](https://github.com/codeforIATI/iati-datastore/pull/106))
- Update README, and add setup instructions ([#107](https://github.com/codeforIATI/iati-datastore/pull/107))

### Changed
- Upgrade to python 3 (and upgrading lots of dependencies) ([#93](https://github.com/codeforIATI/iati-datastore/pull/93))
- Download codelists from https://codelists.codeforiati.org ([#94](https://github.com/codeforIATI/iati-datastore/pull/94))
- Set User-Agent header to "codeforIATI datastore classic" ([#96](https://github.com/codeforIATI/iati-datastore/pull/96))

### Removed
- Remove heroku-specific things ([#103](https://github.com/codeforIATI/iati-datastore/pull/103))

### Fixed
- Updated codelists ([#95](https://github.com/codeforIATI/iati-datastore/pull/95))
- Properly implement CORS ([#100](https://github.com/codeforIATI/iati-datastore/pull/100))
