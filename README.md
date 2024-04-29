# InternetQualityMonitoring

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Tests Status(https://img.shields.io/badge/tests-passing-brightgreen)](https://shields.io/)

## Project Description

In the student community of Innopolis University it is decently well-known
and agreed upon that the internet on campus and some internal services
(like moodle) have been quite unstable recently.


The relevant authorities, however, are not convinced and perpetrate the
narrative that all internet issues are small, local, individual problems.


This service is an easily deployable service with a dashboard and ability
to view data from other instances.

## How to Use (Deploy)

### Docker

```bash
docker build -t iqm . 
docker run -d iqm
```

### Or manually

```bash
sudo apt install net-tools nmap
pip install poetry
poetry install

(poetry run python3 backend/main.py &) && poetry run streamlit run frontend/app.py
```

## Technical Stack

This project uses the following technologies:

- Python3
- Poetry
- Sqllite
- Streamlite
- Docker

## How to Develop

To contribute to this project, follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them
4. Push your changes to your fork
5. Create a pull request to merge your changes into the main repository

## Contribution Guidelines

When contributing to this project, please follow these guidelines:

- Keep the code clean and readable
- Test your changes thoroughly before submitting a pull request
- Follow the project's coding style and best practices

Thank you for your interest in contributing to this project! 

