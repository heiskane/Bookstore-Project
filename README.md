# Bookstore-Project

## Development environment setup 
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

## Docker deployment
```bash
git clone https://github.com/heiskane/Bookstore-Project.git
cd Bookstore-Project/fastapi_backend
docker build -t bookstore_api .
docker run -d --name bookstore_backend -p 8000:80 bookstore_api
```


Api documentation can be found at http://localhost:8000/docs
