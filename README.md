# Smart Parking Management System

## Project Overview

Smart Parking Management System is a cloud-based web application developed using Flask and MySQL. The system allows users to register, login, book parking slots, and view booking history. Administrators can manage users and monitor parking bookings through an admin dashboard.

---

## Features

### User Features
- User Registration
- User Login
- Parking Slot Booking
- Vehicle Number Management
- Booking History
- Logout

### Admin Features
- Admin Login
- View All Users
- View All Bookings
- Manage Parking Slots
- Dashboard Statistics

---

## Technologies Used

### Frontend
- HTML
- CSS
- Bootstrap

### Backend
- Python Flask

### Database
- MySQL

### Cloud Services
- AWS EC2
- AWS S3
- AWS CloudWatch

### DevOps
- Git
- GitHub
- Docker

### Web Server
- Nginx Reverse Proxy

---

## AWS Architecture

User
↓
DuckDNS Domain
↓
Nginx Reverse Proxy
↓
Flask Application
↓
MySQL Database
↓
AWS S3 Bucket

Monitoring:
- AWS CloudWatch

Version Control:
- GitHub Repository

Containerization:
- Docker

---

## Security Features

- Password Authentication
- SQL Injection Prevention using Parameterized Queries
- SSH Key-Based Authentication
- Fail2Ban Protection
- Security Groups Firewall
- HTTPS Configuration using Let's Encrypt
- Nginx Reverse Proxy

---

## Project Screenshots

Screenshots are available in the project report.

---

## Deployment Steps

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure MySQL Database

Create database:

```sql
CREATE DATABASE smartparking;
```

### Run Application

```bash
python3 app.py
```

Application will run on:

```text
http://localhost:5000
```

---

## Docker

Build Docker Image

```bash
docker build -t smart-parking .
```

Run Container

```bash
docker run -d -p 5000:5000 smart-parking
```

---

## Monitoring

AWS CloudWatch is used for:

- EC2 Monitoring
- CPU Usage Monitoring
- Memory Monitoring
- Application Monitoring

---

## Author

Adithyan P M

Internship Capstone Project

Smart Parking Management System
