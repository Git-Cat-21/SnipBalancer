# SnipBalancer

A Load-Balanced URL Shortener

---
<details>
<summary>Week1</summary>

## 1. Set Up a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Create a Docker Network for Redis

```bash
docker network create redis
```

---

## 3. Prepare the Clustering Environment (Navigate to the clustering directory)

```bash
chmod +x script.sh
./script.sh
docker pull redis:7.4.2-alpine
```

---

## 4. Build and Run the SnipBalancer Docker Image

Build the image (development target):

```bash
docker build --target dev -t snipbal .
```

Or build the default image:

```bash
docker build -t snipbal .
```

Run the container:

```bash
docker run -it -v "${PWD}:/work" -p 5000:5000 \
    --net redis \
    -e REDIS_SENTINELS="sentinel-0:5000,sentinel-1:5000,sentinel-2:5000" \
    -e REDIS_MASTER_NAME="mymaster" \
    -e REDIS_PASSWORD="okok" \
    snipbal
```

---

## 5. Check Redis Status

Access a Redis container shell:

```bash
docker exec -it redis-0 sh
```

Connect with Redis CLI:

```bash
redis-cli
auth <password>
KEYS *
GET <key_val>
```

---

## Notes

- Replace `<password>` and `<key_val>` with your password and desired Redis key.

</details>

> **Reference:**  
> This project setup was taken from [this guide](https://github.com/marcel-dempers/docker-development-youtube-series/blob/master/python/introduction/part-5.database.redis/README.md).
