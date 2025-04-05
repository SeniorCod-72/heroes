# Superheroes API

This project is a simple Flask API that allows you to manage and interact with superheroes, their powers, and their associated strengths. The API provides routes to access, update, and create heroes, powers, and hero-power relationships. It utilizes Flask-SQLAlchemy and Flask-Migrate for database management and migrations.

## Features

- **GET /heroes** - Retrieve a list of all heroes.
- **GET /heroes/:id** - Retrieve a single hero by their ID.
- **GET /powers** - Retrieve a list of all powers.
- **GET /powers/:id** - Retrieve a single power by its ID.
- **PATCH /powers/:id** - Update a power's description.
- **POST /hero_powers** - Create a new hero-power relationship with a specified strength.

## Installation

To get started with this project, you'll need to set up a local environment. Follow the steps below:

### Prerequisites

- Python 3.x
- `pip` for installing dependencies
- `SQLite` for the database

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/seniorCod-72/superheroes-api.git
   cd superheroes-api
