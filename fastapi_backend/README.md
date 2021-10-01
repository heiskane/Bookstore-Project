# FastAPI

## Uvicorn deployment (Development)
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
firefox http://localhost:8000/docs
```

## Docker deployment
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
docker build -t bookstore_api .
docker run -d --name bookstore_backend -p 8000:80 -e GUNICORN_CONF="/app/app/gunicorn_conf.py"  bookstore_api
firefox http://localhost:8000/docs
```

Api documentation can be found at http://localhost:8000/docs

### Something to read

* [Paypal Integration](paypal_integration.md)
* [File Upload/Download](files.md)
* [Images](images.md)