## HW 6 SQLAlchemy

## Configuration

### 1. Environment Variables

Create a `.env` file in the root directory of the project to securely store database credentials. The example below:

```env
# .env 
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin1234
POSTGRES_DB=university
PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=admin1234
DATABASE_URL=postgresql://admin:admin1234@db:5432/university
```

### 2. Launch Docker

Start the database, pgAdmin, and the Python application containers:

``` bash
docker-compose up -d --build

docker exec -it python_web_hw_6_app bash
```

### 3. Run Database Migrations & Seed Data

``` bash
# Apply migrations to the latest revision
alembic upgrade head

# Generate and insert dummy data
python seed.py
```

### 4. Run Queries

```bash
# Execute the predefined SQLAlchemy 2.0 select queries
python my_select.py
```

### 5. Access pgAdmin (Optional)

To visually inspect the database structure and data:

- Open your browser and go to `http://localhost:5050`
- Log in using the credentials from your `.env` file.
- Register a new server using the hostname `db` and port `5432`.