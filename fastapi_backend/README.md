# FastAPI

## Something to read

* [Paypal Integration](stuff_to_read/paypal_integration.md)
* [File Upload/Download](stuff_to_read/files.md)
* [Images](stuff_to_read/images.md)


## Deployment

### Docker-Compose Deployment

Make sure right docker-compose version is installed
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Run backend
```bash
cd Bookstore-Project
sudo docker-compose build
sudo docker-compose up -d
```

Update backend
```bash
git pull
sudo docker-compose build
sudo docker-compose down
sudo docker-compose up -d
```

## Testing

Currently there is very limited tests but to run run them make sure you have the backend running and use the following command

```bash
docker-compose exec api /app/tests-start.sh
```

Api documentation can be found at http://localhost:8000/docs


## Database Migrations

Database migrations are done using alembic

```bash
alembic revision --autogenerate -m 'Add columb to blaa'
```

After this the docker-compose deployment will run `alembic upgrade head` to upgrade the database
