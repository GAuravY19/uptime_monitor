# Uptime Monitoring Dashboard

## Overview

This project is a lightweight **Uptime Monitoring Dashboard** built using **FastAPI**, **PostgreSQL**, **HTML/CSS**, and **Bootstrap**.

The application allows users to register websites for monitoring. A background scheduler periodically checks each registered website, records its availability, response time, HTTP status code, and response time difference, and displays the latest monitoring history on a live dashboard.

---

# Features

* Register websites for monitoring
* Automatic monitoring every minute
* Live dashboard updates (without page refresh)
* Track:

  * Website Status (UP / DOWN)
  * HTTP Status Code
  * Response Time
  * Response Time Difference
  * Timestamp
* View the latest 30 monitoring records
* Filter monitoring history by website
* PostgreSQL database backend

---

# Tech Stack

### Backend

* FastAPI
* Python
* PostgreSQL
* Requests
* Jinja2

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript (Fetch API)

---

# Project Structure

```text
project/
│
├── Frontend/
│   ├── index.html
│   └── style/
│       └── style.css
│
├── backend/
│   ├── crud.py
│   ├── database.py
│   ├── helper.py
│   ├── routes.py
│   ├── scheduler.py
│   └── .env
│
├── main.py
├── requirements.txt
├── Dockerfile
├── AI_LOG.md
└── README.md
```

---

# Database

The application uses two tables.

## website_listing

Stores all registered websites.

| Column      | Description        |
| ----------- | ------------------ |
| web_id      | Primary Key        |
| web_name    | Website Name       |
| web_url     | Website URL        |
| under_track | Monitoring Enabled |

---

## website_tracking

Stores monitoring history.

| Column              | Description                       |
| ------------------- | --------------------------------- |
| track_id            | Primary Key                       |
| web_id              | Foreign Key                       |
| url                 | Website URL                       |
| status              | UP / DOWN                         |
| status_code         | HTTP Status Code                  |
| response_time_ms    | Response Time                     |
| response_difference | Difference from Previous Response |
| hit_timestamp       | Monitoring Timestamp              |

---

# Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file inside the `backend` folder.

Example:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=uptime_monitor
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Start the Application

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000
```

---

# Monitoring Logic

Each monitored website is checked every minute.

The monitoring rules are:

* HTTP 2xx → UP
* HTTP 3xx → UP
* HTTP 4xx → UP
* HTTP 5xx → DOWN
* Timeout / DNS Failure / Connection Error → DOWN

Response Difference is calculated as:

```
Current Response Time − Previous Response Time
```

---

# Cloud Deployment Approach

For deploying this MVP, I would containerize the FastAPI application using Docker and deploy it to a managed container platform **Azure Container Apps**.

The overall architecture would be:

```text
Internet
     │
     ▼
Cloud Load Balancer
     │
     ▼
FastAPI Container
     │
     ▼
Managed PostgreSQL Database
```

Deployment steps:

1. Build a Docker image for the FastAPI application.
2. Push the image to a container registry
3. Provision a managed PostgreSQL instance
4. Deploy the container to a managed container service.
5. Configure environment variables for database connectivity.
6. Expose the application through a Load Balancer or managed HTTPS endpoint.
7. Configure health checks to monitor container availability.

This architecture keeps the application stateless, allows horizontal scaling of the FastAPI service, and separates compute from persistent database storage, making it suitable for extending the MVP into a production-ready service.

---

# AI Collaboration

The complete AI collaboration log describing the development process, prompts, architectural decisions, and iterative improvements is available in **AI_LOG.md**.
