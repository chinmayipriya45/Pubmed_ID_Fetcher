# PubMed Paper Fetcher

## Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Clone the repository
3. Run `poetry install` to set up dependencies

## Usage

To fetch papers:

```sh
poetry run get-papers-list "cancer treatment"
```

To save results to a CSV file:

```sh
poetry run get-papers-list "cancer treatment" -f results.csv
```

To enable debug mode:

```sh
poetry run get-papers-list "cancer treatment" -d
```
