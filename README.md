# Automated-ETL-Pipeline
# 🛠️ Data Engineering ETL Pipeline

This project demonstrates a full end-to-end ETL (Extract, Transform, Load) pipeline using Docker, Python, PostgreSQL, and SQL Server.

---

## 📦 Project Structure

```
├── extract_data.py               # Extracts JSON data from public API
├── load_to_postgres.py          # Loads raw data into PostgreSQL staging tables
├── transfer_postgres_to_sqlserver.py # Transfers transformed data to SQL Server
├── Dockerfile                   # Docker build file for Python app
├── docker-compose.yml          # Orchestrates PostgreSQL, SQL Server, and app
├── .env                         # Contains all DB credentials (Postgres + SQL Server)
├── posts.json                   # API response (posts)
├── user.json                    # API response (users)
└── run_pipeline.bat             # [Windows] Full automation of ETL process
```

---

## ⚙️ Setup Instructions

1. ✅ Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and running
2. ✅ Clone/download the project folder
3. ✅ Run the ETL pipeline:
```bash
run_pipeline.bat
```

---

## 🔄 ETL Pipeline Overview

| Step | Description |
|------|-------------|
| 1️⃣   | Extract JSON data from [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com/) using `requests` |
| 2️⃣   | Load into PostgreSQL (`staging_users`, `staging_posts`) |
| 3️⃣   | Transform with SQL JOIN → `transformed_user_posts` |
| 4️⃣   | Load into SQL Server → `FactUserPosts` |

---

## 🧮 Table Schemas

### PostgreSQL

#### `staging_users`
| Column         | Type    |
|----------------|---------|
| id             | INTEGER |
| name           | VARCHAR |
| username       | VARCHAR |
| email          | VARCHAR |
| phone          | VARCHAR |
| website        | VARCHAR |
| company_name   | VARCHAR |
| address_city   | VARCHAR |

#### `staging_posts`
| Column | Type    |
|--------|---------|
| id     | INTEGER |
| userId | INTEGER |
| title  | TEXT    |
| body   | TEXT    |

#### `transformed_user_posts`
| Column      | Type    |
|-------------|---------|
| post_id     | INTEGER |
| post_title  | TEXT    |
| post_body   | TEXT    |
| user_name   | VARCHAR |
| user_email  | VARCHAR |

---

### SQL Server

#### `FactUserPosts`
| Column      | Type         |
|-------------|--------------|
| post_id     | INT          |
| post_title  | NVARCHAR(MAX)|
| post_body   | NVARCHAR(MAX)|
| user_name   | NVARCHAR(255)|
| user_email  | NVARCHAR(255)|

---

## ✅ Design Decisions

- Used `.env` file and `os.environ` for secret management
- Docker Compose orchestrates all services
- Logging + retries added for stability
- Default PostgreSQL and SQL Server containers used for simplicity
- Project supports modular, script-based execution

---

## 🧪 Testing

- Manual validation of row counts in both PostgreSQL and SQL Server
- Schema verified using SQL queries
