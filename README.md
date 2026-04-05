# Acxhange Library Management System

The **Acxhange Library Management System** simplifies internal library workflows through an intuitive and interactive web interface. It improves accessibility and efficiency for both employees and administrators.

---

## ✨ Features

* Browse Complete Book Catalog Online
* Search and Filter Books Easily
* Request Books Directly from the Web App
* Track Request Status
* Admin Panel for Managing Books and Requests
* Responsive and User-Friendly UI

---

## 🛠️ Tech Stack

**Frontend**

* Angular

**Backend**

* FastAPI

**Database**

* MySQL

**Deployment**

* Cloud-based (Serverless Architecture)

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.13
* Node.js & npm
* MySQL Server

---

### 🔧 Backend Setup (FastAPI)

```bash
# Clone the repository
git clone https://github.com/thisisyashvanth/Acx-Lib-Final-In-Progress.git
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate    

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Run the server
uvicorn main:app --reload
```

---

### 🔐 Environment Variables

This project uses a `.env` file for configuration (e.g., database credentials, secrets).

* The `.env` file is **not committed to version control** for security reasons
* A `.env.example` file **is included in the repository as a template**
* Copy it and update the values before running the application

```bash
cp .env.example .env
```

### 💻 Frontend Setup (Angular)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
ng serve
```

Visit: `http://localhost:4200`

---

### Database Setup (MySQL)

1. Create a Database:

```sql
CREATE DATABASE acx_lms_db;
```

2. Update Database Credentials in `.env`

---

## Usage

1. Open the Angular URL
2. Signup for an Account with acxhange.com Domain
3. Login to the Portal with Email & Password
4. View the Book Catalogue
5. Create a Request of Your Wish (Borrow, Renew, Return)
6. Collect Book from Library Upon Approval from HR

---

## Project Structure

```
acx_lms/
│
├── backend/           # FastAPI Backend
│   ├── app/
│   ├── models/
│   ├── routes/
│   └── main.py
│
├── frontend/          # Angular Frontend
│   ├── src/
│   └── angular.json
│
└── README.md
```
---

## Roadmap

* Notification System Integration
* Download Data as Excel
  
---

## Troubleshooting

* Ensure MySQL Service is Running
* Verify `.env` File is Correctly Configured
* Check API Base URL in Angular Environment Files

---