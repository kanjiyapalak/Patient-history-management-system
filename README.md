# 🏥 Patient History Management System

A web-based Patient History Management System built using **Django**. It supports role-based access for **Doctors**, **Patients**, and **Receptionists**, enabling management of appointments, prescriptions, and patient profiles.

---

## 📌 Features

### 🔐 Authentication
- User login and signup
- Role-based login (Doctor, Patient, Receptionist)

### 🧑‍⚕️ Doctor
- Register, update, and delete profile
- Add, update, delete prescriptions for patients
- View appointments with assigned patients

### 🧑 Patient
- View profile
- View own prescriptions
- View their own appointments

### 🧑‍💼 Receptionist
- Add appointments for patients with doctors

---

## 🛠 Tech Stack

- **Backend**: Django 4.x
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS (Django Templates)
- **Authentication**: Django Auth System

---

## 📁 Project Structure

```
DJANGO_PROJECT/
├── manage.py
├── db.sqlite3
├── patient_history/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── templates/
├── static/
```

---

## 📋 Setup Instructions

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/your-username/patient-history-management.git
cd patient-history-management
```

### 2. 🐍 Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. 📦 Install Dependencies

```bash
pip install django
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. ⚙️ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 👤 Create Superuser

```bash
python manage.py createsuperuser
```

### 6. 🚀 Start the Server

```bash
python manage.py runserver
```

Visit the app at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Common Commands

| Task              | Command                            |
|-------------------|-------------------------------------|
| Install Django    | `pip install django`                |
| Run server        | `python manage.py runserver`        |
| Apply migrations  | `python manage.py migrate`          |
| Make migrations   | `python manage.py makemigrations`   |
| Create superuser  | `python manage.py createsuperuser`  |

---

## 👥 User Roles Summary

| Role         | Permissions                                                                 |
|--------------|-------------------------------------------------------------------------------|
| **Doctor**   | Register, update/delete profile, manage prescriptions, view appointments     |
| **Patient**  | View profile, view prescriptions, view their appointments                    |
| **Receptionist** | Add appointments by selecting doctor & patient                          |

---

## ✅ Future Enhancements

- Appointment reminders (email or SMS)
- Patient search/filter
- Export prescriptions and reports to PDF

---

## 🙏 Thank You

Thanks for checking out the Patient History Management System!  
Feedback and contributions are welcome. Feel free to open issues or submit pull requests.
