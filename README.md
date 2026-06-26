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
│   ├── dashboard.html
│   └── style/
│       └── dashboard.css
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

## Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/GAuravY19/uptime_monitor.git
cd .\uptime_monitor\
```

### 2. Configure Environment Variables

A Google Drive link containing the required `.env` file will be shared via email.

* Download the `.env` file.
* Place it in the following directory:

```
backend/.env
```

### 3. Build and Start the Application

Run the following command from the project root:

```bash
docker compose up --build
```

This will:

* Build the Docker image.
* Install all required dependencies.
* Start the FastAPI application.
* Launch the background website monitoring scheduler.

### 4. Access the Application

Once the containers are running successfully, open your browser and navigate to:

```
http://localhost:8000
```

### 5. Stop the Application

To stop the application, press:

```text
Ctrl + C
```

or, if running in detached mode:

```bash
docker compose down
```

---

## Verification Guide

To verify the uptime monitoring logic, use the following test cases after starting the application.

### Step 1: Start the Application

Run the FastAPI application and ensure the scheduler is active.

Open the dashboard:

```text
http://127.0.0.1:8000
```

---

### Step 2: Register a Healthy Website

Add the following website:

| Name    | URL                 |
| ------- | ------------------- |
| Google | https://www.google.com/ |
| Flipkart | https://www.flipkart.com/ |
| Meesho | https://www.meesho.com/ |

Expected Result:

* Status → **UP**
* HTTP Status Code → **200**
* Response Time → A numeric value (e.g., 120 ms)
* Response Difference → Calculated after the second monitoring cycle

---

### Step 3: Register an Unreachable Website

Add an invalid or unreachable URL, for example:

| Name    | URL                                  |
| ------- | ------------------------------------ |
| Det | https://doing.com/ |

Expected Result:

* Status → **DOWN**
* HTTP Status Code → --
* Response Time → --
* Response Difference → --

---

### Step 4: Wait for Scheduler

The monitoring scheduler executes every **60 seconds**.

After one monitoring cycle, the dashboard automatically refreshes and displays the latest monitoring results.

---

### Expected Behaviour

Healthy website:

```text
Status          : UP
HTTP Code       : 200
Response Time   : X ms
```

Unreachable website:

```text
Status          : DOWN
HTTP Code       : --
Response Time   : --
```

---

### HTTP Status Handling

The monitoring logic follows these rules:

| HTTP Response                            | Status |
| ---------------------------------------- | ------ |
| 2xx                                      | UP     |
| 3xx                                      | UP     |
| 4xx                                      | UP     |
| 5xx                                      | DOWN   |
| Timeout / DNS Failure / Connection Error | DOWN   |

This allows the application to distinguish between a reachable server returning an application error (5xx) and a completely unreachable endpoint.

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
