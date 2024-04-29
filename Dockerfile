FROM duffn/python-poetry:3.11-slim

EXPOSE 8501
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
COPY backend/*.py /app/backend/
RUN apt update && \
    apt install -y nmap iputils-ping && \
    poetry install

CMD ["(poetry run python3 backend/main.py &) &&", "poetry run streamlit run", "backend/app.py"]
