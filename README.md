# CareerBoost 🚀

A comprehensive career development platform empowering users to plan, track, and achieve their professional goals with AI-driven insights, real-time mentorship, and a polished user experience.

---

## 📖 About CareerBoost

CareerBoost is an all-in-one web application designed to streamline career advancement for students, early-career professionals, and career switchers. It integrates personalized job recommendations, skill development, professional branding, and community support into one unified experience.

Built with **React**, **Supabase**, and **PostgreSQL**, it delivers a scalable, cloud-based solution with a sleek, modern interface.

---

## ✨ Key Features

| Feature                           | Description                                                     |
| --------------------------------- | --------------------------------------------------------------- |
| 🎯 Interactive Career Roadmap     | Dynamic visual timeline of goals, courses, and job applications |
| 📊 Skill Mastery Dashboard        | Animated radial bars to track skill proficiency                 |
| 🤖 AI-Powered Job Recommendations | Tailored listings based on skills and goals                     |
| 📚 Learning Paths                 | Curated course collections aligned with your career plan        |
| 📄 Resume & Portfolio Builder     | PDF resume generator and shareable project portfolio            |
| ✅ Task & Goal Tracking            | Set milestones, divide into tasks, track progress visually      |
| 🎤 Mock Interview Simulator       | AI-generated feedback on interview answers                      |
| 💬 Real-Time Mentorship Chat      | Live chat with mentors and peers                                |
| 🧠 Community Forum                | Ask questions, share insights, build your network               |
| 📈 Analytics & Contests           | Track growth and compete in skill challenges                    |

---

## 🌟 Problem Statement

Today’s job market is filled with fragmented tools—job boards, MOOCs, resume builders, etc.—which can leave users overwhelmed and isolated. CareerBoost addresses these challenges by:

* Guiding users with a clear career roadmap
* Bridging skill gaps with smart recommendations
* Enhancing employability with professional outputs
* Fostering support through mentorship and forums
* Motivating action via analytics and gamification

---

## 🛠️ Tech Stack

| Category           | Technology                                                    |
| ------------------ | ------------------------------------------------------------- |
| **Frontend**       | React, Tailwind CSS, React Spring, React Circular Progressbar |
| **Backend**        | Supabase (PostgreSQL, PostgREST, Supavisor)                   |
| **Database**       | PostgreSQL (RLS, JSONB, Triggers)                             |
| **Real-Time**      | Supabase WebSockets, Socket.IO (for Mentorship Chat)          |
| **File Storage**   | Supabase Storage (S3-compatible)                              |
| **Authentication** | Supabase Auth (JWT, Email, OAuth)                             |
| **PDF Generation** | jsPDF (Resumes, Portfolios)                                   |
| **Deployment**     | Vercel (Frontend), Supabase Cloud (Backend)                   |

---

## 🖼️ Screenshots

| Dashboard                               | Skill Mastery                                   | Portfolio                               | Mentorship Chat                                     |
| --------------------------------------- | ----------------------------------------------- | --------------------------------------- | --------------------------------------------------- |
| ![Dashboard](screenshots/dashboard.png) | ![Skill Mastery](screenshots/skill-mastery.png) | ![Portfolio](screenshots/portfolio.png) | ![Mentorship Chat](screenshots/mentorship-chat.png) |

---

## 🚀 Getting Started

### ✅ Prerequisites

* Node.js v16 or higher
* Supabase account
* GitHub account

---

### 🧰 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/careerboost.git
cd careerboost

# Install dependencies
npm install
```

---

### 🔑 Environment Setup

1. Create a project in [Supabase](https://supabase.com)
2. Go to **Project Settings > API** and copy:

   * Project URL
   * Anon Key
3. Create a `.env` file in root:

```env
REACT_APP_SUPABASE_URL=your-supabase-url
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
```

---

### 🧱 Database Setup

```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY,
  email TEXT,
  skills TEXT[] DEFAULT '{}',
  skill_mastery JSONB DEFAULT '[]'
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
```

> More SQL available in `database/setup.sql`

---

### ▶️ Start the App

```bash
npm start
```

Open in browser: [http://localhost:3000](http://localhost:3000)

---

### 💬 (Optional) Real-Time Chat Server (Mock)

```bash
npm install -g json-server
json-server --watch db.json --port 3001
```

---

## 📂 Project Structure

```bash
careerboost/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js
│   │   ├── SkillMastery.js
│   │   ├── Portfolio.js
│   │   └── People.js
│   ├── styles/
│   │   ├── styles.css
│   │   ├── SkillMastery.css
│   │   └── Portfolio.css
│   ├── supabaseClient.js
│   └── App.js
├── database/
│   └── setup.sql
├── .env
├── package.json
└── README.md
```

---

## 🔧 Usage Guide

| Action               | Description                                 |
| -------------------- | ------------------------------------------- |
| **Sign Up/Login**    | Register with email or OAuth                |
| **Set Career Goals** | Define goals like “Become a Web Developer”  |
| **Track Skills**     | Monitor skill growth via dashboard          |
| **Find Jobs**        | View AI-driven job recommendations          |
| **Build Resume**     | Export polished resumes using jsPDF         |
| **Add Projects**     | Upload and showcase projects in a portfolio |
| **Mock Interviews**  | Practice interviews with AI feedback        |
| **Mentorship**       | Chat live with mentors                      |
| **Community**        | Ask and answer in the forum                 |
| **Analytics**        | View visual feedback on progress            |

---

## 🏆 Hackathon Highlights

| Highlight      | Description                                           |
| -------------- | ----------------------------------------------------- |
| 💡 Innovation  | AI + mentorship + community + roadmap in one platform |
| 🌍 Impact      | Helps users overcome real career obstacles            |
| ✨ UI Polish    | Modern fonts, React Spring animations, responsive     |
| ⚙️ Scalability | Serverless backend with Supabase and WebSockets       |

---

## 🔮 Future Enhancements

* 🔍 AI job matching with embeddings & pgvector
* 📱 Mobile app with React Native
* 🏅 Gamification (badges, leaderboard)
* 📊 Advanced analytics & trends dashboard
* 🏢 Enterprise-level team support features

---

## 🤝 Contributing

We welcome contributions!

```bash
# Fork the repo
# Create a feature branch
git checkout -b feature/YourFeature

# Commit changes
git commit -m "Add YourFeature"

# Push branch
git push origin feature/YourFeature

# Open a Pull Request 🎉
```

Please follow our Code of Conduct and open issues via GitHub Issues.

---

## 📜 License

Licensed under the [MIT License](LICENSE)

---

## 🙌 Acknowledgements

* [Supabase](https://supabase.com)
* [React](https://reactjs.org)
* [React Spring](https://react-spring.dev/)
* \[Hackathon Organizers] for inspiration

---

## 📬 Contact

**Author:** Your Name
**GitHub:** [@yourusername](https://github.com/yourusername)
**Email:** [your.email@example.com](mailto:your.email@example.com)
**LinkedIn:** [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)

---

> **CareerBoost:** Your Career, Your Plan, Your Success! 🌟
