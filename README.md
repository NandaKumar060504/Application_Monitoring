# 📊 Application Monitoring Dashboard

This project is a **Log Analytics Platform** designed to collect, process, and visualize log data in real-time using Dockerized components. It features real-time log ingestion, structured storage, and insightful dashboards.

## 🚀 Project Overview

The platform leverages:

- **Apache Kafka** for real-time log ingestion
- **Relational Databases** for storing processed log data
- **Grafana** for querying and visualizing logs and metrics

## ✅ Functional Requirements

- 🔁 **Request Count per Endpoint**: Tracks how many times each API endpoint is called.
- ⏱ **Response Time Trends**: Shows latency patterns over time.
- ❌ **Frequent Errors**: Identifies and highlights common application errors.
- 📺 **Live Log Feed**: Displays logs in real-time for monitoring.

*You can add more dashboards to enhance monitoring based on your needs.*

## ⚙️ Non-Functional Requirements

- All components are containerized with **Docker** for portability and scalability.

## 🧰 Technology Stack

| Component       | Tool             |
|----------------|------------------|
| Containerization | Docker          |
| Message Broker   | Apache Kafka    |
| Visualization    | Grafana         |
| Optional DBs     | Prometheus, Loki|

## 🛠️ Implementation Steps

### Week 1: Infrastructure & API Setup

- Develop or use a REST API server (5–10 endpoints).
- Generate API requests with a load script.
- Set up Kafka topics for different log types.
- Implement a Kafka producer to push logs.
- Dockerize all components.

### Week 2: Log Processing & Storage

- Build a Kafka consumer to process logs and store them.
- Design schema and configure databases.

### Week 3: Visualization

- Connect Grafana to the database.
- Write queries for dashboard metrics.
- Configure alerting/monitoring panels.

## 📚 Resources

- [json-server (REST API mock)](https://github.com/typicode/json-server)
- [Kafka on Docker (Official Docs)](https://docs.docker.com/guides/kafka/)
- [Confluent Kafka Tutorials](https://developer.confluent.io/confluent-tutorials/kafka-on-docker/)
- [Prometheus](https://prometheus.io/)
- [Loki (for logs)](https://grafana.com/docs/loki/latest/)
- [ELK Stack Overview](https://elastic-stack.readthedocs.io/en/latest/introduction.html)
- [PLG Stack Intro](https://raman-pandey.medium.com/plg-prometheus-loki-grafana-stack-for-apps-monitoring-eef8dc702da1)

## 📌 Notes

- You can use any language/framework to build your API.
- Stack is customizable — feel free to integrate better-suited tools.
- Explore alternative stacks like ELK or PLG based on use case.

---

> 📂 Once you're ready, push your files and this `README.md` to GitHub for a complete and professional repo!

Let me know if you'd like badges, diagrams, or deployment instructions added!
