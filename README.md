# ANEES | AI-Powered Autism Therapy Platform

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Top 27 MENA](https://img.shields.io/badge/Award-Top_27_MENA-gold)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

**ANEES** is a comprehensive platform designed to bridge the gap between therapists and families of children with autism. It utilizes Artificial Intelligence to assist in monitoring progress and suggesting therapeutic interventions, streamlining the therapy management process.

## 🏆 Achievements
* **Ranked Top 27 in MENA Region**: Recognized for innovation and social impact.
* **Grade A+**: Graduation Project Excellence.

## 🚀 Key Features
* **AI-Assisted Analysis**: Integrated Machine Learning models to analyze patient behavior patterns.
* **Therapist Dashboard**: Centralized management for patient files, progress reports, and appointment scheduling.
* **Secure Data Handling**: HIPAA-compliant data structure for sensitive medical records.
* **RESTful API**: Robust backend serving mobile and web clients.
* **Containerized Deployment**: Fully Dockerized for consistent environments.

## 🛠️ Tech Stack
* **Backend Framework:** Django & Django REST Framework (DRF)
* **Database:** PostgreSQL
* **AI/ML:** Python (Integration with ML models)
* **DevOps:** Docker, Docker Compose
* **Authentication:** JWT (JSON Web Tokens)

## 🔧 Installation & Run

### Prerequisites
* Docker & Docker Compose installed.

### Steps
1.  **Clone the repository**
    ```bash
    git clone https://github.com/bassiony1/public-ANEES.git
    cd public-ANNES
    
    ```
2. ** Add your Anees/.env.prod and Anees/.env.db for the prod settings
3.  **Build and Run with Docker**
    ```bash
    docker-compose up --build
    ```
4.  **Access the Application**
    * API Root: `http://localhost:8000/api/`
    * Admin Panel: `http://localhost:8000/admin/`

## 🤝 Contributing
Contributions are welcome. Please open an issue to discuss proposed changes.
