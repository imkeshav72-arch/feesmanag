# 🎓 College Fees Management System — Mini College Project

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python + Flask
- **Database**: SQLite (auto-created, no setup needed)

---

## 📁 Project Structure

```
fees-app/
├── backend/
│   ├── app.py            ← Flask backend + SQLite DB
│   └── requirements.txt  ← Python dependencies
├── frontend/
│   └── index.html        ← Frontend UI
└── README.md
```

---

## ⚙️ Setup Instructions

### Step 1 — Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Run Backend
```bash
python app.py
```
Backend runs at: http://localhost:5000
SQLite database `fees.db` is created automatically.

### Step 3 — Open Frontend
Open `frontend/index.html` in any browser.

---

## 🔗 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/students` | Get all students |
| POST | `/students` | Add new student |
| DELETE | `/students/<id>` | Delete student |
| GET | `/fees` | Get all fee records |
| POST | `/fees` | Add fee payment |
| DELETE | `/fees/<id>` | Delete fee record |
| GET | `/stats` | Dashboard statistics |

---

## ✨ Features
- Add / Delete Students
- Record Fee Payments (Tuition, Exam, Hostel, etc.)
- Payment Modes: Cash, UPI, Cheque, DD, Online
- Status Tracking: Paid / Pending / Partial
- Dashboard with total stats
- Search & filter students and records
- SQLite database (no extra setup)

---

## 👨‍💻 Made for Mini College Project
