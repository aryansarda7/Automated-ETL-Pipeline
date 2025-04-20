FROM python:3.12-slim

WORKDIR /app

# Install ODBC dependencies
RUN apt-get update && \
    apt-get install -y gcc g++ gnupg curl unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    pip install --no-cache-dir psycopg2-binary pyodbc

COPY . .

CMD ["python", "transfer_postgres_to_sqlserver.py"]
