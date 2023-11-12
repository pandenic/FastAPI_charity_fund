# Description
Project is used for charity projects foundation. It supports creation of charity projects and investing donations buy other users. 

The project uses 

| Technologies | Links |
| ---- | ---- |
| ![git_Flask](https://github.com/pandenic/Shortcut_URL/assets/114985447/340e1027-f1e0-4d0b-a5b1-d2286e89fbd0) | [Flask](https://flask.palletsprojects.com/en/3.0.x/) |
| ![git_SQLAlchemy](https://github.com/pandenic/Shortcut_URL/assets/114985447/3d49ecef-6014-4e87-8a39-8e3f62660a98) | [SQLAlchemy](https://www.sqlalchemy.org/) |
| ![git_SQLite](https://github.com/pandenic/Shortcut_URL/assets/114985447/9305dc46-66c1-4e5a-a1e4-3167e676780a)| [SQLite](https://www.sqlite.org/index.html) |


# Installation


Clone repository:
```bash
git clone
```
Go to the project directory:
```
cd cat_chsrity_fund
```
Create and activate venv:

```bash
python3.9 -m venv venv
```

- for Linux/macOS

    ```bash
    source venv/bin/activate
    ```

- for windows

    ```bash
    source venv/scripts/activate
    ```

Install requirements in the backend folder:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Start a project locally from an app root directory:
```bash
uvicorn main:app --reload 
```

# Request examples
(for more information you could use a swaggers doc at http://127.0.0.1:8000/docs or file `openapi.json` at project root direction) 


Create a user:
```Curl
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}'
```

Create a charity project (for a superuser):  
```Curl
curl -X 'POST' \
  'http://127.0.0.1:8000/charity_project/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMSIsImF1ZCI6WyJmYXN0YXBpLXVzZXJzOmF1dGgiXSwiZXhwIjoxNjk5ODA0MjgxfQ.vguqpuln7-ND1y8Al2l9Xldjong3tSWNTCQc9_GFsk8' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string23",
  "description": "string",
  "full_amount": 100
}'
```

Login:
```Curl
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/jwt/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=qwe&password=qweqwe1&scope=&client_id=1&client_secret=1'
```

Create a donation:
```Curl
curl -X 'POST' \
  'http://127.0.0.1:8000/donation/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMSIsImF1ZCI6WyJmYXN0YXBpLXVzZXJzOmF1dGgiXSwiZXhwIjoxNjk5ODA0MjgxfQ.vguqpuln7-ND1y8Al2l9Xldjong3tSWNTCQc9_GFsk8' \
  -H 'Content-Type: application/json' \
  -d '{
  "full_amount": 50,
  "comment": "string"
}'
```
