# Back-End-Development-Songs

Songs microservice — Flask REST API backed by MongoDB, built for the IBM Back-End Development Capstone Project (Course 11 of the IBM Back-End Development Professional Certificate).

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check (pings MongoDB) |
| GET | `/song` | List all songs |
| POST | `/song` | Create a song (`title`, `artist`) |
| GET | `/song/<id>` | Get one song |
| PUT | `/song/<id>` | Update a song |
| DELETE | `/song/<id>` | Delete a song |

## Run locally

```bash
# start MongoDB first
pip install -r requirements.txt
python app.py        # serves on http://localhost:5002
```

## Tests

```bash
pytest -v
```

## Docker

```bash
docker build -t songs-service .
docker run -p 5002:5002 --link mongo:mongo songs-service
```
