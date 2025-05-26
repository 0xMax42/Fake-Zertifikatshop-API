# Changelog

All notable changes to this project will be documented in this file.

## [0.4.0] - 2025-05-26

### 🚀 Features

- *(workflows)* Add release workflow and enhance nightly build - (d1c4001)
- *(config)* Enhance production server configuration - (e0b5ff1)
- *(workflows)* Add nightly Docker build and push workflow - (5b82a24)

### 🐛 Bug Fixes

- *(workflows)* Correct Docker image tag casing in nightly build - (3eb76bf)

## [0.3.1] - 2025-05-26

### 🚀 Features

- *(seed)* Add new product certifications - (386854b)
- *(backend)* Add stock management for products - (2424118)
- *(api)* Add OpenAPI 3.0 specification for product management - (d10c2c1)
- *(admin)* Add basic authentication and admin setup - (4dea2a6)
- *(dependencies)* Add sqladmin with full extras and related deps - (e29c232)

### 🚜 Refactor

- *(cliff)* Simplify template logic and align formatting - (a78b404)

### 📚 Documentation

- *(readme)* Add note on configuring admin credentials - (1225a8e)

## [0.2.0] - 2025-05-26

### 🚀 Features

- *(docker)* Add Dockerfile for building and running the Python app with Poetry - (abe9230)
- *(backend)* Add product management API with CRUD operations - (9e00be4)
- *(seed)* Add product seeding script for database initialization - (5abc85d)
- *(database)* Add SQLite database initialization and session support - (410bb19)
- *(models)* Add product models for database integration - (d112f78)
- *(project)* Add pyproject.toml with dependencies and tasks - (2ae75d1)
- *(scripts)* Add Gitea automation scripts for CI workflows - (4284fcb)

### 📚 Documentation

- Add project setup and usage instructions in README - (abed855)

### 🧪 Testing

- *(tests)* Add API integration tests for product endpoints - (9ccb664)

### ⚙️ Miscellaneous Tasks

- *(project)* Update project name in pyproject.toml - (5dcc0da)
- *(project)* Add changelog generation script to pyproject toml - (b72189e)
- *(config)* Add default git-cliff configuration - (300a5d4)
- *(vscode)* Customize activity bar and peacock colors - (a53a2f3)
- *(gitignore)* Add ignore rules for db, cache, and pycache - (496a53a)


