# Upgrading the Database to PostgreSQL

This document outlines the steps to upgrade the database from SQLite to PostgreSQL.

## 1. Install PostgreSQL

Ensure you have PostgreSQL installed and running on your system.

## 2. Install the PostgreSQL driver

Install the `psycopg2-binary` driver:

```bash
pip install psycopg2-binary
```

Add `psycopg2-binary` to your `requirements.txt` file.

## 3. Create a PostgreSQL database

Create a new PostgreSQL database for this project.

## 4. Update the database URL

Update the `SQLALCHEMY_DATABASE_URL` in your `.env` file to point to your new PostgreSQL database. For example:

```
SQLALCHEMY_DATABASE_URL=postgresql://user:password@host:port/database
```

## 5. Run the migrations

Run the Alembic migrations to create the schema in your new PostgreSQL database:

```bash
alembic upgrade head
```
