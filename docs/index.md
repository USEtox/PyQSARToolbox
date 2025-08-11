# PyQSARToolbox

PyQSARToolbox is a lightweight Python client for interacting with a locally running **QSAR Toolbox** Web API instance.

## Features

* Discover calculators, QSAR models, profilers, workflows, metabolism simulators.
* Search chemicals by CAS, name, SMILES, or internal IDs.
* Retrieve endpoint trees, metadata, and experimental data.
* Apply QSAR models and profiling operations programmatically.

## Installation

```bash
pip install pyqsartoolbox
```

For development (tests + docs):

```bash
pip install -e .[dev]
```

## Quick Start

```python
from pyqsartoolbox import QSARToolbox

# Replace with your local toolbox port
qs = QSARToolbox(port=62008)
print(qs.toolbox_version())

chem = qs.search_name("benzene")[0]
print(chem["ChemId"], chem["Names"])
```

## Documentation

[Get started here!](getting-started.md)
