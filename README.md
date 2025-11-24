# Hospital Appointment and Patient Management System

A Django-based web application for managing hospital appointments, patients, and doctors. This project provides a simple UI for patients to book appointments and for doctors/admins to manage schedules and patient records.

---

## Live Demo

🚀 [**Live Demo:**](https://hospital-appointment-and-patient.onrender.com) 


---

## Table of Contents

* [About](#about)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Repository Structure](#repository-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Running the Project](#running-the-project)
* [Database & Admin](#database--admin)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)

---

## About

This project implements a basic hospital management system with appointment booking and patient management functionality. It is suitable as a learning project or a starting point for a more advanced healthcare system.

## Features

* Patient registration and profile management
* Doctor profiles and availability
* Appointment booking and cancellation
* Basic admin dashboard for managing doctors, patients, and appointments
* Static assets (CSS/JS/images) and templates for UI

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite (default for development)
* **Others:** Django templating, static/media handling

## Repository Structure

```
Hospital-Appointment-and-Patient-Management-System/
├─ HospitalManagment/        # Main Django project settings
├─ accounts/                  # User authentication & profiles
├─ doctors/                   # Doctor app (profiles, schedules)
├─ patients/                  # Patient app (records, appointments)
├─ static/                    # Static files (CSS, JS, images)
├─ templates/                 # HTML templates
├─ db.sqlite3                 # Development SQLite DB
├─ manage.py
├─ requirements.txt
├─ LICENSE
└─ README.md
```

## Requirements

See `requirements.txt` for the Python package dependencies. Typical requirements include:

* Django
* Pillow (if image uploads are used)
* django-crispy-forms or similar (optional)

You can install dependencies with:

```bash
pip install -r requirements.txt
```

> Note: Use a virtual environment (venv) to avoid polluting your global Python installation.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yanayem/Hospital-Appointment-and-Patient-Management-System.git
cd Hospital-Appointment-and-Patient-Management-System
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. (Optional) Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

## Running the Project

Start the development server:

```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/` to view the application.

## Database & Admin

* The project uses SQLite by default for development (`db.sqlite3` is included in the repo). For production use, switch to PostgreSQL or another production-ready database.
* Access the Django admin at `/admin/` and use the superuser account created earlier to log in.

## Usage

* Register as a patient account (or have an admin create doctor accounts).
* Patients can browse available doctors and book appointments.
* Doctors/admins can view upcoming appointments and manage patient records.

##

## Contributing

Contributions are welcome! If you'd like to add features or fix bugs:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to your branch and open a Pull Request

Please follow standard GitHub PR practices and include clear descriptions and screenshots where applicable.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
