# InternetQualityMonitoring

## Install

```bash
pip install poetry
poetry install
```

## Run

```bash
poetry run streamlit run frontend/app.py
```

## Testing 

Coverage testing

```bash
poetry run pytest --cov=backend/
```

Mutation testing

```bash
poetry run mutmut run --paths-to-mutate "backend/" --tests-dir "tests/"
poetry run mutmut show
```
