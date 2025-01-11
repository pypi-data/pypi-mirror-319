# pkdb_data: python utilities for PK-DB data
[![Version](https://img.shields.io/pypi/v/pkdb_data.svg)](https://pypi.org/project/pkdb_data/)
[![MIT License](https://img.shields.io/pypi/l/pkdb_data.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/pkdb_data.svg)](https://pypi.org/project/pkdb_data/)

This repository stores the curated study data for [https://pk-db.com](https://pk-db.com) and provides helpers for uploading studies to the database.

* [`./studies/`](./studies/): curated study data with subfolders based on substances
* [`./docs/CURATION.md`](./docs/CURATION.md): curation guidelines and documentation


# Documentation
Documentation such as installation instructions are available from
[`./docs/CURATION.md`](./docs/CURATION.md>)

## Functionality in a nutshell
The following provides a short overview of the main functionality.

### Upload study
To upload a study use
```bash
upload_study -s <study_dir>
```

### Upload studies
A set of studies can be uploaded via

```bash
upload_studies -s caffeine
```

# License
- Source Code: [MIT](https://opensource.org/license/MIT)
- Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

# Funding
Matthias König (MK) was supported by the Federal Ministry of Education and Research (BMBF, Germany) within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054). MK is supported by the Federal Ministry of Education and Research (BMBF, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA).

© 2017-2025 Jan Grzegorzewski & Matthias König
