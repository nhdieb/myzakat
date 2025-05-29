
# 🌟 MyZakat.org — Zakat Distribution Foundation Website

![Built with Flask](https://img.shields.io/badge/Built%20with-Flask-000000?logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Hosted on PythonAnywhere](https://img.shields.io/badge/Hosted-PythonAnywhere-blue)

---

---

# 📆 Table of Contents

1. 📚 Project Summary
2. 🛠️ Installation & Setup Guide
3. ☁️ Temporary Deployment (PythonAnywhere)
4. 📊 Deployment Flow Diagrams
5. 🚩 Launch Roadmap Checklist
6. 📧 Public Launch Email Template
7. 📰 Press Release Template
8. 📃 Launch Day Checklist

---

# 1. 📚 Project Summary

MyZakat.org is the official platform for the Zakat Distribution Foundation (ZDF), dedicated to alleviating poverty, supporting orphans, refugees, and empowering communities through Zakat and Sadaqa donations.

**Key Features:**
- Zakat Calculator
- Secure Donations
- Volunteer Sign-Up
- Admin Dashboard for managing submissions, donations, volunteers, and events
- Mobile-responsive and professionally structured

**Tech Stack:** Flask, SQLAlchemy, Flask-Login, Flask-Mail, SQLite, HTML5/CSS3, JavaScript

---

# 2. 🛠️ Installation & Setup Guide

## 1. Clone the Repository
```bash
git clone https://github.com/yourusername/myzakat.org.git
cd myzakat.org
```

## 2. Create a Virtual Environment
```bash
python -m venv venv
```
Activate:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Database Setup
```bash
flask db upgrade
```
(Or migrate if fresh.)

## 5. Run Locally
```bash
python run.py
```
Visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

# 3. ☁️ Temporary Deployment (PythonAnywhere)

1. Create an account at pythonanywhere.com.
2. Upload project files.
3. (Optional) Setup a virtualenv.
4. Configure WSGI file:
```python
import sys
path = '/home/yourusername/myzakat'
if path not in sys.path:
    sys.path.append(path)

from run import app as application
```
5. Map static files.
6. Reload.

Visit: `https://yourusername.pythonanywhere.com/`

---

# 4. 📊 Deployment Flow Diagrams

### Basic Flow (PythonAnywhere)
```
Local Machine -> GitHub (optional) -> PythonAnywhere -> Live Site
```

### Full Production Flow
```
Local Machine -> GitHub -> VPS (Gunicorn + Nginx + SSL) -> myzakat.org
```

---

# 5. 🚩 Launch Roadmap Checklist

### Phase 1: Final Testing
- Check all pages
- Test all forms
- Backup database

### Phase 2: Temporary Hosting
- Upload to PythonAnywhere
- Test with friends

### Phase 3: Production Deployment
- VPS setup (Ubuntu)
- Gunicorn + Nginx
- SSL with Let's Encrypt
- Domain connection

### Phase 4: Launch
- Social media announcements
- Email to supporters
- Monitor live site

---

# 6. 📧 Public Launch Email Template

**Subject:** 🌟 Exciting News! MyZakat.org is Now Live!

**Body:**
> Assalamu Alaikum,
>
> I'm thrilled to announce the launch of **MyZakat.org**, the new platform of the Zakat Distribution Foundation.
>
> Learn, calculate, donate, and volunteer today!
>
> Visit: [https://myzakat.org](https://myzakat.org)
>
> May Allah bless you for your support!
>
> — [Your Name]

---

# 7. 📰 Press Release Template

**FOR IMMEDIATE RELEASE**

**Zakat Distribution Foundation Launches MyZakat.org**

Alexandria, VA — The ZDF announces the launch of MyZakat.org, empowering Muslims to fulfill Zakat and Sadaqa obligations easily.

The platform features:
- Zakat Calculator
- Secure donations
- Volunteer sign-up
- Upcoming events

Visit [https://myzakat.org](https://myzakat.org) to learn more.

---

# 8. 📃 Launch Day Checklist

### Night Before
- Check pages/forms/mobile responsiveness
- Backup instance/ folder
- Prepare social posts & email

### Launch Morning
- Launch site publicly
- Post on social media
- Send launch email
- Test site live

### Launch Week
- Thank early donors
- Share with Islamic centers
- Start Ramadan Campaign planning

---

# 🌟 YOU ARE READY TO LAUNCH!

May your project be blessed and impactful, inshaAllah! 🙏🏼

