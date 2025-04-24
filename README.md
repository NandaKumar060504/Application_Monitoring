# 📊 Application Monitoring Dashboard

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/NandaKumar060504/Application_Monitoring)
[![Dockerized](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)

A real-time **Log Analytics Platform** that ingests, stores, and visualizes logs and metrics using a modern containerized stack. Built for scalable application monitoring.

---

## 🚀 Project Overview

The platform includes:

- **Kafka** for real-time log ingestion
- **Relational DB(s)** for structured log storage
- **Grafana** for dashboard creation and visualization
- Entire stack is containerized using **Docker**

---

## ✅ Functional Requirements

- 🔁 **Request Count per Endpoint**
- ⏱ **Response Time Trends**
- ❌ **Most Frequent Application Errors**
- 📺 **Live Real-Time Logs**

---

## ⚙️ Non-Functional Requirements

- Full containerization for all components via Docker
- Easily deployable and scalable microservices architecture

---

## 🧰 Technology Stack

| Component       | Tool             |
|----------------|------------------|
| Containerization | Docker          |
| Message Broker   | Apache Kafka    |
| Visualization    | Grafana         |
|  DataBases       |    Mysql        |

---

## 🛠️ Implementation Steps

### Week 1: Infrastructure & API Setup

- Develop or use a REST API server (5–10 endpoints)
- Generate API requests to simulate load
- Kafka setup with topics for log types
- Kafka producer for log ingestion
- Docker setup for all services

### Week 2: Log Processing & Storage

- Kafka consumer for log processing
- Database schema design and storage implementation

### Week 3: Dashboard Visualization

- Connect Grafana to DB
- Create metric-based dashboards
- Implement monitoring panels

---

## 📦 Deployment Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/NandaKumar060504/Application_Monitoring.git
cd Application_Monitoring
docker-compose up --build

## Team :
1. Nanda Kumar T (PES1UG22CS375)
2. P Ashish (PES1UG22CS404)
3. Prajwal N P (PES1UG22CS423)
4. Pavan T R (PES1UG22CS411)
