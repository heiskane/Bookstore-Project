# FastAPI

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


### Uvicorn deployment (Deprecated)
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
firefox http://localhost:8000/docs
```

### Docker deployment (Deprecated)
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
docker build -t bookstore_api .
docker run -d --name bookstore_backend -p 8000:80 bookstore_api
firefox http://localhost:8000/docs
```

Api documentation can be found at http://localhost:8000/docs

### Something to read

* [Paypal Integration](paypal_integration.md)
* [File Upload/Download](files.md)
* [Images](images.md)


## Database Migrations

Database migrations are done using alembic

```bash
alembic revision --autogenerate -m 'Add columb to blaa'
```

After this the docker-compose deployment will run `alembic upgrade head` to upgrade the database
