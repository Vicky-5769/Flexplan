# 💪 FlexPlan – Full-Stack Fitness Website

**Final Year Project** | Flask + MongoDB + HTML/CSS/JS

---

## 🚀 Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Frontend  | HTML5, CSS3, Vanilla JavaScript   |
| Backend   | Python Flask                      |
| Database  | MongoDB (via PyMongo)             |
| Auth      | Session-based + Werkzeug hashing  |

---

## 📁 Project Structure

```
flexplan/
├── app.py                  # Flask backend (routes + API)
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # All styles (dark theme, responsive)
│   └── js/
│       └── main.js         # Auth state + nav active link
└── templates/
    ├── base.html           # Shared navbar + footer
    ├── index.html          # Home page
    ├── workouts.html       # Workout Library (Dumbbell + Bodyweight)
    ├── diet.html           # South Indian Diet Plans (7-day tables)
    ├── progress.html       # Progress Tracker
    ├── bmi.html            # BMI Calculator
    ├── login.html          # Login page
    └── register.html       # Register page
```

---

## ⚙️ Setup Instructions

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Start MongoDB

Make sure MongoDB is running locally:

```bash
# macOS/Linux
mongod

# Windows
net start MongoDB
```

Or use MongoDB Atlas (cloud) — update `MONGO_URI` in app.py.

### 3. Run the Flask app

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🌟 Features

### 🏠 Home Page
- Hero section with stats (15+ workouts, 6 diet plans, 100% free)
- Feature cards linking to all sections
- Fitness tips grid (nutrition, recovery, training, mindset)

### 🏋️ Workout Library (`/workouts`)
- **2 workout types**: Dumbbell & Bodyweight
- **3 levels**: Beginner 🟢 | Intermediate 🟡 | Pro 🔴
- Search & filter functionality
- Exercise cards with sets, reps, calories, equipment
- Full 6-day training plan per level

### 🥗 Diet Plans (`/diet`)
- **South Indian Diet Planner** with 3 goals:
  - 💪 Muscle Gain (2,800–3,200 kcal/day)
  - 🥦 Weight Loss (1,400–1,700 kcal/day)
  - 🍛 Weight Gain (3,000–3,500 kcal/day)
- Full 7-day meal tables with Breakfast, Lunch, Dinner, Pre/Post-Workout
- Modal popup with complete diet table
- Filter by goal

### 📊 Progress Tracker (`/progress`)
- Login required to save data
- Log workouts with name, exercise, weight, height, calories
- Auto-calculates BMI
- Statistics: total workouts, calories burned, average BMI
- Delete entries

### 🧮 BMI Calculator (`/bmi`)
- Metric (kg/cm) and Imperial (lbs/ft) units
- Real-time BMI result with category & color
- Personalized recommendations

### 🔐 Authentication
- Register / Login / Logout
- Session-based authentication
- Password hashing (Werkzeug)
- Protected routes (progress tracker requires login)

---

## 🗄️ MongoDB Collections

| Collection | Description                        |
|------------|------------------------------------|
| `users`    | User accounts (username, email, hashed password) |
| `progress` | Workout logs (workout, weight, height, BMI, calories, date) |

---

## 🎨 Design

- **Dark theme** (#0d0f14 background, #f97316 orange accent)
- **Fonts**: Bebas Neue (headings) + Barlow (body)
- **Responsive** — works on mobile, tablet, desktop
- Inspired by the FitForge UI reference screenshots

---

## 📝 API Endpoints

| Method | Endpoint           | Description              | Auth Required |
|--------|--------------------|--------------------------|---------------|
| POST   | `/api/register`    | Create new account       | No            |
| POST   | `/api/login`       | Login                    | No            |
| POST   | `/api/logout`      | Logout                   | No            |
| GET    | `/api/me`          | Get current user         | No            |
| GET    | `/api/progress`    | Get all progress logs    | Yes           |
| POST   | `/api/progress`    | Add progress log         | Yes           |
| DELETE | `/api/progress/:id`| Delete a progress log    | Yes           |

---

## 🏫 Final Year Project Notes

- All workout data sourced from uploaded docx files
- South Indian diet plans (muscle gain, weight loss, weight gain)
- 6-day dumbbell + bodyweight routines (beginner/intermediate/pro)
- MongoDB used for persistent user data and progress logs
- Flask RESTful API backend with session authentication
