# 🚀 FastAPI Starter CLI

A CLI tool for generating FastAPI projects with predefined structure and automatic configuration.

## ✨ Main Features

### 📁 Project Generation
- Create new project with predefined structure
- Initialize project in existing directory
- Automatic file and directory generation

### 🛢️ Multi-Database Support
- PostgreSQL
- MySQL/MariaDB
- SQL Server
- Oracle
- Automatic connection configuration

### ⚙️ Automatic Configuration
- Python virtual environment
- Custom requirements.txt
- Environment variables (.env)
- Pydantic Settings
- SQLModel ORM

### 🔧 Additional Features
- Alembic migrations (optional)
- Base Repository for CRUD (optional)
- Modular and scalable structure
- FastAPI best practices integration

## 🚀 Main Commands

```bash
# Create new project
fastapi start create-project

# Initialize in current directory
fastapi start init-project

# Show version
fastapi cli version
```

## 📦 Generated Structure
```
project/
├── src/
│   ├── controller/      # API Controllers
│   │   └── __init__.py
│   ├── service/         # Business Logic
│   │   └── __init__.py
│   ├── repository/      # Data Access
│   │   └── __init__.py
│   ├── model/          # Domain Models
│   │   ├── entity/     # SQLModel Entities
│   │   │   └── __init__.py
│   │   ├── enum/       # Enumerations
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── dto/            # Data Transfer Objects
│   │   └── __init__.py
│   ├── config/         # Configuration
│   │   ├── settings.py
│   │   └── __init__.py
│   ├── db/            # Database Config
│   │   ├── database.py
│   │   └── __init__.py
│   ├── main.py        # Entry Point
│   └── __init__.py
├── test/              # Unit Tests
│   └── __init__.py
├── .env              # Environment Variables
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## 📦 Optional Packages
- Alembic - SQL Migrations
- SQLAlchemy Base Repository - Base CRUD

## ⚙️ Requirements
- Python 3.8+
- pip (package manager)
- Compatible database installed

## 🚀 Installation

```bash
pip install fastapi-starter-cli
```

## 📝 License
MIT License

## 👤 Author
betooo