# imfp

[![Tests](https://github.com/chriscarrollsmith/imfp/actions/workflows/test.yml/badge.svg)](https://github.com/chriscarrollsmith/imfp/actions/workflows/test.yml)
[![PyPI Version](https://img.shields.io/pypi/v/imfp.svg)](https://pypi.python.org/pypi/imfp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`imfp`, by Christopher C. Smith, is a Python package for downloading data from the [International Monetary Fund's](http://data.imf.org/) RESTful JSON API.

**[📚 Full Documentation](https://promptlytechnologies.com/imfp/)**

## Installation

```bash
pip install -q --upgrade imfp
```

## Quick Start

```python
import imfp

# Get list of available databases
databases = imfp.imf_databases()

# Get parameters for a specific database (e.g., PCPS - Primary Commodity Price System)
params = imfp.imf_parameters("PCPS")

# Fetch data with specific parameters
df = imfp.imf_dataset(
    database_id="PCPS",
    freq=["A"],
    start_year=2000,
    end_year=2015
)
```

## Key Features

- Comprehensive access to IMF's extensive economic databases
- Parameter discovery
- Rate limit and bandwidth management
- Returns data in pandas DataFrames

## Contributing

We welcome contributions to improve `imfp`! Here's how you can help:

1. If you find a bug, please open an issue
2. To fix a bug:
   - Fork the repository
   - Create a fix
   - Open a pull request to the `dev` branch

Note that you will need to install the [Poetry](https://python-poetry.org/docs/#installation) package manager to install the dependencies and run the tests, and the [Quarto CLI tool](https://quarto.org/docs/download/) to render the documentation.

## Maintainers

To deploy a new version:
1. Increment version with `poetry version patch/minor/major`
2. Update dependencies with `poetry update`
3. Run tests with `pytest tests`
4. Update documentation if needed
5. Push to dev
6. Open PR to main

To render and deploy documentation:
1. `quarto render`
2. `quarto publish`

The GitHub Actions workflow will handle code formatting, testing, and deployment to PyPI after merge.
