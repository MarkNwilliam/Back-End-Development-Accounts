# Back-End-Development-Accounts

Accounts REST API Service

[![CI Build](https://github.com/MarkNwilliam/Back-End-Development-Accounts/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/MarkNwilliam/Back-End-Development-Accounts/actions/workflows/ci-build.yaml)

## Project Overview

This project implements a RESTful API for managing accounts with CI/CD pipeline, Docker containerization, and Kubernetes deployment.

## Features

- REST API for CRUD operations on accounts
- CI/CD with GitHub Actions
- Security headers with Talisman and CORS
- Docker containerization
- Kubernetes deployment
- Tekton CD pipeline

## Setup

```bash
pip install -r requirements.txt
PYTHONPATH=. python service/init_db.py
gunicorn --bind 0.0.0.0:8000 service:app
```

## Testing

```bash
nosetests
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Index |
| GET | /health | Health check |
| POST | /accounts | Create account |
| GET | /accounts | List accounts |
| GET | /accounts/:id | Get account |
| PUT | /accounts/:id | Update account |
| DELETE | /accounts/:id | Delete account |
