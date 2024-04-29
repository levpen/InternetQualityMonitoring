FROM python:3.11-buster

EXPOSE 8501
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
COPY backend/*.py /app/backend/
RUN pip install poetry && apt update && \
    apt install -y nmap iputils-ping && \
    poetry install

CMD ["poetry", "run", "streamlit", "run", "backend/app.py"]
