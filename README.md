# Northwind Data Engineering & Analytics Portfolio

A comprehensive, end-to-end data engineering and analytics portfolio project built around the classic **Northwind Traders** relational database. This repository demonstrates the transition from traditional operational database management (OLTP) to modern analytical data warehousing (OLAP Star Schema) and programmatic data manipulation using Python and Pandas.

## Why an OLAP Star Schema? 

Operational databases (OLTP like northwind_oltp) are optimized for row-level transactional integrity, fast writes, and normalization (3NF), which makes complex analytical aggregation slow and query-heavy. By transforming and loading this data into an analytical Star Schema (northwind_olap), we decouple reporting workloads from production systems, pre-joining dimensions (dim_customers, dim_products, dim_time) with a central fact table (fact_sales) to accelerate analytical queries.

## Declarative & Programmatic Governance

Rather than relying on manual scripts or brittle Jupyter notebooks, this pipeline utilizes object-oriented design principles, custom file-system-aware logging (pathlib & inspect), and environment segregation. This ensures end-to-end traceability and reproducibility.

## Actionable Business Intelligence Theory 

Data engineering is only as valuable as the decisions it unlocks. This project implements standard enterprise metrics—such as Pareto Analysis (The 80/20 Rule) for inventory management, Recency/Frequency/Monetary (RFM) Segmentation, and Multi-Series Seasonality Forecasting—to translate raw bytes into executive-ready insights.

---

## 📋 Project Architecture & Roadmap

```
|-- datasets/         # Raw database initialization scripts
|-- logs/             # Local exports of diffrent log files
|-- python_analysis/  # Python scripts for Pandas/OLTP
|-- sql_analysis/     # SQL scripts
|-- .gitignore        # Files that git should never track
|-- .README           # Quick summary of the project
|-- .requiremnts      # Necessary libraries
```

## 🛠️ Local Environment & Database Setup
If you are running this project locally (or in a development container like GitHub Codespaces), follow these steps to set up the databases:

```bash
# In the terminal install PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

```bash
# Start the PostgreSQL:

#For github codespace
# Open quick access with ctrl + shift + p and type
~/.bashrc
# Paste this line
pg_isready -q || sudo service postgresql start

#For linux
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

```bash
# Open the prompt as the postgres user
sudo -u postgres psql

# Create the databases
createdb northwind_oltp
createdb northwind_olap

# Give the postgres user a password
ALTER USER postgres PASSWORD '12345';

# Run the raw northwind.sql file inside your datasets directory
sudo -u postgres psql -d northwind_oltp -f northwind.sql
sudo -u postgres psql -d northwind_olap -f northwind.sql

# Install a PostgrSQL extension
# Configurate the database source
Username=postgres
Password=12345
Server_Address=localhost
Port=5432
Database=northwind

# Install libraries:
pip install -r requirements.txt
```


## ⚙️ Environment Configuration(OPTIONAL)

For certain files like upload_to_s3.py you will need to create a aws account there a s3 bucket with access keys and .env file and update it with your AWS credentials

```
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=your_aws_region
AWS_BUCKET_NAME=your_bucket_name
```
