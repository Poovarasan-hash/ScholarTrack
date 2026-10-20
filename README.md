# ScholarTrack — Scholarship & Fellowship Deadline Tracker

ScholarTrack is a full-stack web application designed to help students discover, monitor, match, and track application deadlines for scholarships and fellowships.

---

## 🌟 Key Features

- **Scholarships Directory**: Search, filter by category and education level, and sort opportunities by deadline, amount, or relevance.
- **Eligibility Checker**: Real-time illustrative eligibility scoring that evaluates GPA, academic level, and state criteria.
- **Application Progress Tracker**: Track application stages from interested to submitted, under review, and approved.
- **Student Dashboard**: Live summary of upcoming deadlines, application stats, and personalized recommendations.
- **Authentication**: Secure registration, login, session management with HTTP-only cookies, password hashing (via Werkzeug), and CSRF protection.
- **Responsive UI**: Built with HTML5, CSS3, Bootstrap 5, and vanilla JavaScript following an accessible Sage Green / Emerald theme.

---

## 🛠️ Tech Stack

### Frontend
- HTML5 / Semantic Web
- CSS3 (Custom design system with CSS custom properties)
- Bootstrap 5.3 & Bootstrap Icons
- Vanilla JavaScript (Modular ES6+)
- GSAP for subtle reveals

### Backend
- Python 3 / Flask
- PyMySQL
- python-dotenv
- Werkzeug security
- Flask-CORS

### Database
- MySQL 8.0 (InnoDB, `utf8mb4`) with dual-mode SQLite local fallback

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- MySQL Server 8.0+

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ScholarTrack.git
cd ScholarTrack
```

### 3. Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Set up Environment Variables:
   Copy `.env.example` to `.env` in the `backend/` directory:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Update `backend/.env` with your database credentials:
   ```env
   SECRET_KEY=your-secure-random-key
   FLASK_ENV=development
   PORT=5000
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=scholartrack_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   ```

4. Initialize the MySQL Database:
   Execute the schema migration script in your MySQL shell or client:
   ```bash
   mysql -u root -p scholartrack_db < backend/models/schema.sql
   ```

5. Run the Application:
   ```bash
   python backend/app.py
   ```
   The application will start at `http://127.0.0.1:5000/`.

---

## 📁 Project Structure

```
ScholarTrack/
│
├── frontend/
│   ├── index.html                   # Landing page
│   ├── login.html                   # Student login
│   ├── signup.html                  # Student registration
│   ├── dashboard.html               # Main student dashboard
│   ├── scholarships.html            # Scholarship search & browse
│   ├── scholarship-details.html     # Detailed view & requirements
│   ├── eligibility.html             # Eligibility scoring & matching
│   ├── applications.html            # Application status tracker
│   ├── profile.html                 # Student academic profile
│   ├── contact.html                 # Help & FAQs
│   ├── css/
│   │   ├── style.css                # Global theme & typography
│   │   └── auth.css                 # Authentication styles
│   └── js/
│       ├── main.js                  # Global application scripts
│       ├── auth.js                  # Authentication controller
│       └── animations.js            # Page transitions & reveals
│
├── backend/
│   ├── app.py                       # Flask entrypoint & route registration
│   ├── config.py                    # Environment & database configuration
│   ├── requirements.txt             # Python dependencies
│   ├── controllers/
│   │   └── auth_controller.py       # Auth endpoints & sessions
│   ├── models/
│   │   ├── database.py              # Database connection & query execution
│   │   ├── schema.sql               # Full database DDL schema
│   │   └── migrate_missing_tables.sql
│   └── services/
│       └── auth_service.py          # Business logic & password verification
│
├── .gitignore
└── README.md
```

---

## 🔒 Security Best Practices
- Passwords are encrypted using Scrypt/PBKDF2 via Werkzeug.
- HTTP-only session cookies prevent XSS session hijacking.
- `.env` and database files are excluded from version control.
