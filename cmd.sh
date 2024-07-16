docker pull postgres
docker pull python:3.9

docker compose up -d --build

# docker compose down

# Get container
docker ps

# Enter inside of the container
docker exec -it skutopia-challenge-db-1 bash

# Start query console
psql -U postgres

# Define password
ALTER ROLE postgres WITH PASSWORD 'mypassword';

# docker run -d --name skutopia-postgres-container -p 5432:5432 -e POSTGRES_PASSWORD=mypassword postgres

# docker exec -it skutopia-postgres-container psql -U postgres \l

psql -U postgres

docker-compose up --build

