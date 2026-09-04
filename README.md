# Facial Recognition Attendance System (FRAS)

A web-based attendance system that replaces manual roll-call with automated, camera-based face recognition. An admin registers students through a Django web panel; a separate script then uses a webcam to detect and recognize faces in real time, logging attendance automatically to a daily CSV file.

## Features

- Admin login (Django authentication)
- Register, edit, and delete student records (roll no, enrollment no, name, phone, gender, stream, photo)
- Real-time face detection and recognition via webcam
- Automatic attendance logging with roll no, name, date, and time
- Duplicate-proof: a student is logged only once per day

## Tech Stack

| Tool | Purpose |
|---|---|
| Django 5.2 | Web framework, admin panel, ORM |
| MySQL 8.0 | Relational database |
| OpenCV | Webcam capture and frame drawing |
| dlib | Underlying face-detection and encoding models |
| face_recognition | Python wrapper for face matching |
| python-decouple | Loads secrets from `.env` |

## Project Structure

```
fras/
├── admin_panel/          # Models, views, forms, templates for the admin panel
├── attendance_system/    # Django project settings and URL config
├── attendance/            # Daily attendance CSV files (generated at runtime)
├── media/                 # Uploaded student photos (generated at runtime)
├── recognize.py           # Standalone webcam recognition script
├── manage.py
├── requirements.txt
└── .env.example            # Template for required environment variables
```

## Prerequisites

- Python 3.10+
- MySQL Server 8.0 (Community Edition) with MySQL Workbench recommended
- A webcam (for the recognition script)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Ritam000/Facial-recognition-attendance-system.git
cd Facial-recognition-attendance-system
```

### 2. Install MySQL

Download and install MySQL Community Server from [dev.mysql.com](https://dev.mysql.com/downloads/installer/). During setup:
- Choose the **Full** setup type (installs MySQL Workbench too)
- Keep the default port `3306`
- Set a root password and remember it

### 3. Create the databases

Open MySQL Workbench (or the MySQL Shell), connect as `root`, and run:

```sql
CREATE DATABASE student_registration;
CREATE DATABASE student_attendance;
```

### 4. Set up environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and fill in your own values:

```
SECRET_KEY=any-random-string-you-want
DB_PASSWORD=your-own-mysql-root-password
DB_NAME_REAL=student_registration
DB_NAME_TEST=student_attendance
```

> `SECRET_KEY` can be any random string, it just needs to exist. `DB_PASSWORD` must be **your own** local MySQL root password, not a shared one.

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
pip install python-decouple
```

> If `opencv-python` fails to install, open `requirements.txt` and make sure the version is `opencv-python==4.10.0.84` (older, more broadly compatible versions install cleanly across platforms).

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username and password.

### 8. Run the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in with the superuser account you just created.

### 9. Register students

From the admin panel, click **Add Student** and register each student with a clear, front-facing photo. Recognition accuracy depends heavily on photo quality.

### 10. Run face recognition

In a separate terminal (keep the server running), from the project root:

```bash
python recognize.py
```

This opens your webcam. Detected and matched faces are logged automatically to `attendance/<Day>-<Date>.csv`. Press **Esc** to close the webcam window.

## Known Limitations

- Runs locally only (`127.0.0.1`); not deployed to a public server
- `recognize.py` must currently be run manually from a terminal; for real-world use it should run as a background service (see Future Scope)
- Recognition accuracy depends on photo quality, lighting, and face angle
- Deleting a student removes their database record but not their photo file from `media/`

## Future Scope

- Automated notifications to parents/faculty on absence
- ERP / LMS integration for institutional use
- In-app attendance dashboard instead of raw CSV files
- Improved accuracy via multiple training photos and liveness detection

## License

This project is for academic purposes. Add a license of your choice (e.g., MIT) if you intend for others to reuse the code.
