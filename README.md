# University Course Selection System

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/release)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)

---

## Overview

**University Course Selection System** is a comprehensive web application designed to facilitate various university services for students, including course selection, unit adjustment, course presentation, academic transcript viewing, and more. Developed using Django and Django Rest Framework, the system employs PostgreSQL as the database and incorporates additional tools as outlined in the project description.

## Key Features

- **User profiling:** User can be student, it-manager, pofessor or educational-assistance.
- **Course Registration:** Enable students to easily select and register for courses for the upcoming semester.
- **Unit Adjustment (Add/Drop):** Facilitate the process of adjusting enrolled units, allowing for both addition and removal of courses.
- **Course Information:** Display detailed information about available courses, helping students make informed decisions.
- **Academic Transcript:** Provide students with access to their academic history, including grades and course completion status.
- **Emergency Unit Drop:** Allow for emergency removal of enrolled units under specific circumstances.

## Technologies Used

- **Python 3.12**
- **Poetry:** For package management
- **Django 4.2.6**
- **Django Rest Framework**
- **PostgreSQL**
- **Redis:** For the cache backend
- **Celery:** For task queue
- **MinIo:** For object storage
- **Pytest:** For unit and integration testing
- **Translation**
- **Swagger:** For api documentation
- **Docker and docker-compose:** For containerization the prerequisites and the django app itself

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/GriffinCoders/EDU.git`
2. Install dependencies: `poetry install`
3. Run the prerequisites: `docker-compose up -d`
4. Set up the database: `python manage.py migrate`
5. Run the development server: `python manage.py runserver`

---

Feel free to explore the codebase and contribute to the enhancement of this University Course Selection System! If you encounter any issues or have suggestions, please open an [issue](https://github.com/GriffinCoders/EDU/issues).
