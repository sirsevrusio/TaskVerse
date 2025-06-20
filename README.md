# 🗂️ Taskverse

**Taskverse** is a modern, minimal task management web app built with Flask, HTML5, CSS, and JavaScript.  
Designed with simplicity in mind, it allows users to quickly **add**, **view**, and **complete** tasks with smooth UI interactions and visual feedback.

> Made with ❤️ by [@SirSevrusIO](https://github.com/sirsevrusIO)

---

## 🚀 Features

- 📆 Add tasks with deadline (date and time)
- ✅ Mark tasks as completed via "Done" button
- 🕒 Automatically formats time to AM/PM for display
- 💡 Flash messages for action feedback (success/error)
- 🎨 Clean and responsive UI with animations
- 📜 Sort tasks by deadline
- 🗑️ Dynamic task removal with instant UI update
- 🔒 No login or database setup required (for local use)

---

## 🧠 Why was Taskverse made?

Taskverse was created to:
- Learn and practice full-stack web development using Flask
- Build an offline-first, lightweight task manager
- Experiment with DOM manipulation and async interactions using vanilla JS
- Serve as a base template for more advanced productivity tools

---

## 📦 How It Works

### ▶️ Running Locally

1. **Clone the repository:**

```bash
git clone https://github.com/sirsevrusIO/Taskverse.git
cd Taskverse
```

2. **Create a virtual environment:**
<mark> ** Not Necesaary for Windows Users.** </mark>
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Setup the Server:**

```bash
python TaskVerse.py init
```

5. **Run the Application**
```bash
python TaskVerse.py run
```

---

## 📁 Project Structure

```
Taskverse/
├── TaskVerse.py               # Main Flask app
│
├── templates/
│   ├── homextasks.html       # Main UI template
│   └── 404.html 
├── static/
│   └── css
│       ├── task.css        # CSS styling
│       └── 404.css
├── data
│    └── schedule.json # File containing tasks
├── libs
│     └── utils.py # helper logic
├── requirements.txt
└── README.md
```

---

## ⚙️ Future Plans

- 📅 Task reminders or notifications
- 📊 Weekly productivity analytics
- ☁️ Cloud/database integration (SQLite, Firebase, etc.)

---

## 📄 License

**Taskverse** is open-source and free to use for **personal and educational** purposes.  
However, **commercial use or resale** of this project is **not permitted**.

```
© 2025 SirSevrusIO. All rights reserved.

You may:
✔️ Use, modify, and share this project for non-commercial purposes
❌ Not use it for commercial gain or resale without permission
```

For permissions beyond this license, please contact [SirSevrusIO](https://github.com/sirsevrusIO).

---

## 🌟 Star This Repo

If you find Taskverse useful or inspiring, please consider giving it a ⭐ on GitHub — it helps a lot!

---

## 🙌 Acknowledgements

Thanks to:
- Flask and Python community
- Open source contributors & designers
- Allah ﷻ for giving the ability and motivation to build

---
