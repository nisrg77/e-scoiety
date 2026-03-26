# ✨ eSociety: Premium Gated Community Management ✨

Welcome to **eSociety**, a state-of-the-art management system designed for modern residential complexes. Built with a focus on high-end aesthetics (**Luminous Ledger Design**) and robust backend logic, eSociety provides a seamless experience for Admins, Residents, and Security personnel.

---

## 🎨 Design Philosophy: Luminous Ledger
eSociety isn't just a management tool; it's a premium experience. The entire frontend utilizes the **Luminous Ledger Design System**, featuring:
- **Glassmorphism**: Elegant translucent UI elements with subtle backdrop blurs.
- **Vibrant Aesthetics**: A curated color palette that feels alive and premium.
- **Dynamic Interactions**: Smooth hover effects and micro-animations for an interactive feel.
- **Modern Typography**: Powered by the **Inter** font family for maximum readability.

---

## 🚀 Key Features

### 🏢 Global Society Management (`core`, `residents`)
- **Custom User Authentication**: Secure, email-based login system with role-based access control (Admin, Resident, Security).
- **Society Hierarchy**: Full organizational tracking from Building wings down to individual Flats.
- **Resident Profiles**: Detailed profiles including Family Member tracking and Vehicle registration.
- **Secure Password Recovery**: Robust OTP-based password reset flow via email.

### 🛡️ Security & Emergency Control (`security`, `visitors`)
- **Functional Security Terminal**: A real-time dashboard for gate guards to manage society access.
- **Live Visitor Log**: Track every guest, delivery person, or maintenance worker with check-in/check-out timestamps.
- **Panic Alerts**: Instant emergency notifications (Fire, Medical, Security) that bypass normal queues to alert security immediately.
- **Quick Check-In**: Streamlined registration form for rapid visitor processing at the gate.

### 📅 Resident Portals & Facility Booking (`facilities`, `residents`)
- **Resident Dashboard**: A personal hub for residents to see their community status at a glance.
- **Amenity Reservations**: Real-time booking system for society facilities (Gym, Clubhouse, Pool) with payment status tracking.

### 💰 Finance & Maintenance (`finance`)
- **Automated Invoicing**: Generation of monthly maintenance bills and project-specific charges.
- **Transaction Tracking**: Secure payment logging tied to individual invoices.
- **Society Expenses**: Transparent tracking of society's outgoing expenditures for administrative review.

### 📢 Communication & Governance (`notifications`, `complaints`)
- **Interactive Notice Board**: Pinned announcements and community-wide updates.
- **Community Polls**: A democratic voting system for society-wide decisions.
- **Complaint Management**: Ticketing system for plumbing, electrical, or general maintenance issues with resolution tracking.

---

## 🛠️ Technical Stack
- **Backend**: Python / Django (Modern MVC architecture)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (Luminous Ledger System)
- **Database**: PostgreSQL (Fully configured for production-grade reliability)
- **Email**: Integrated SMTP support for emergency OTP delivery.

---

## ⚙️ Project Setup

### 1. Requirements
Ensure you have Python 3.x installed. The project uses a virtual environment for dependency management.

### 2. Database Configuration
The project is configured for **PostgreSQL**.
- Update the `DATABASES` section in `esociety/settings.py` with your local Postgres credentials (`USER`, `PASSWORD`, `HOST`, `PORT`).
- Database Name: `esoc_db`

### 3. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd esociety

# Setup Virtual Environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate
```

### 4. Running the Project
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to get started!

---

## 🔑 Access Details
For quick verification of the three core roles, refer to **`test_usr.txt`** in the root directory. It contains valid credentials for:
- **Admin**: Full control over all society modules.
- **Resident**: Access to personal dashboard, bookings, and alerts.
- **Security**: Access to the functional guard terminal and visitor logs.

---

## 🚢 Deployment
For detailed instructions on moving to a production server (Nginx/Gunicorn/PostgreSQL), please refer to the **`deploy.txt`** file.

---
*Built with ❤️ by the eSociety Team*
