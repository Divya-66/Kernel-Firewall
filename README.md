# 🚀 CareerBoost

**CareerBoost** is a comprehensive career development platform empowering users to plan, track, and achieve their professional goals with AI-driven insights, real-time mentorship, and a polished user experience.

---

## 📖 About CareerBoost

CareerBoost is an all-in-one web application designed to streamline career advancement for students, early-career professionals, and career switchers. By integrating personalized job recommendations, skill development, professional branding, and community support, CareerBoost transforms the fragmented career journey into a unified, engaging experience.

**Built With:**  
- **Frontend:** React, Tailwind CSS, React Spring  
- **Backend:** Supabase (PostgreSQL), PostgREST  
- **Database:** PostgreSQL with RLS, JSONB, and triggers  
- **Deployment:** Vercel (Frontend), Supabase Cloud (Backend)  

---

## 🌟 Key Features

- 🎯 **Interactive Career Roadmap:** Visualize your journey with a timeline of goals, courses, and applications.  
- 📊 **Skill Mastery Dashboard:** Animated progress bars to measure and highlight skill proficiency.  
- 🤖 **AI-Powered Job Recommendations:** Smart job suggestions tailored to your profile and goals.  
- 📚 **Learning Paths:** Curated course recommendations aligned with your career aspirations.  
- 📄 **Resume & Portfolio Builder:** Export PDF resumes and showcase projects with live links.  
- ✅ **Task & Goal Tracking:** Set milestones, break into tasks, and visualize your progress.  
- 🎤 **Mock Interview Simulator:** Practice with AI-generated questions and real-time feedback.  
- 💬 **Real-Time Mentorship Chat:** Connect instantly with mentors or peers for career advice.  
- 🌐 **Community Forum:** Share insights, ask questions, and engage with a professional network.  
- 📈 **Analytics & Contests:** Track progress and participate in challenges to stay motivated.  

---

## 🎯 Problem Statement

In today's competitive landscape, career development is fragmented across job boards, MOOCs, resume tools, and networking apps—resulting in:

- Skill gaps and inefficiencies  
- Lack of personalized direction  
- Disconnected experiences  
- Low accountability and motivation  

**CareerBoost** solves these with a unified platform that:

- Guides users with a personalized career roadmap  
- Recommends targeted resources to bridge gaps  
- Builds polished professional outputs  
- Fosters mentorship and community  
- Encourages consistency via analytics and gamification  

---

## 🛠️ Tech Stack

| Category         | Technologies Used |
|------------------|-------------------|
| **Frontend**     | React, Tailwind CSS, React Spring, React Circular Progressbar |
| **Backend**      | Supabase (PostgreSQL, PostgREST, Supavisor) |
| **Database**     | PostgreSQL (RLS, JSONB, Triggers) |
| **Real-Time**    | Supabase WebSockets, Socket.IO |
| **Auth**         | Supabase Auth (JWT, Email, OAuth) |
| **PDF Generation** | jsPDF |
| **File Storage** | Supabase Storage (S3-compatible) |
| **Deployment**   | Vercel (Frontend), Supabase Cloud (Backend) |

---

## 🖼️ Screenshots

> *(Add your actual image paths in place of placeholders)*

```markdown
![Dashboard](screenshots/dashboard.png)
![Skill Mastery](screenshots/skill-mastery.png)
![Portfolio](screenshots/portfolio.png)
![Mentorship Chat](screenshots/mentorship-chat.png)
🚀 Getting Started
✅ Prerequisites
Node.js v16 or higher

Supabase account

GitHub account

🧰 Installation
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/careerboost.git
cd careerboost

# Install dependencies
npm install
🔑 Environment Setup
Create a new project in Supabase.

Go to Project Settings > API and copy:

Project URL

Anon Key

Create a .env file in the root directory:

env
Copy
Edit
REACT_APP_SUPABASE_URL=your-supabase-url
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
🧱 Database Setup
Run the SQL setup file via Supabase SQL Editor or manually:

sql
Copy
Edit
CREATE TABLE profiles (
  id UUID PRIMARY KEY,
  email TEXT,
  skills TEXT[] DEFAULT '{}',
  skill_mastery JSONB DEFAULT '[]'
);
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
More SQL available in database/setup.sql

▶️ Start the App
bash
Copy
Edit
npm start
Open your browser at: http://localhost:3000

💬 (Optional) Real-Time Chat Server (Mock)
bash
Copy
Edit
npm install -g json-server
json-server --watch db.json --port 3001
📁 Project Structure
pgsql
Copy
Edit
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
🔧 Usage Guide
Sign Up/Login – Register with email or OAuth

Set Career Goals – Define goals like "Become a Web Developer"

Track Skills – Use the dashboard to view progress

Find Jobs – Get personalized job suggestions

Build Resume – Export professional resumes via jsPDF

Add Projects – Create a shareable online portfolio

Practice Interviews – Use mock simulator with feedback

Get Mentorship – Chat in real-time with mentors

Forum Engagement – Share and learn in the community

Use Analytics – Track your full journey visually

🏆 Hackathon Highlights
💡 Innovation: Combines AI personalization, mentorship, and community in one place

🌍 Impact: Helps users overcome barriers with actionable tools

✨ UI Polish: Smooth animations (React Spring), responsive design, and modern fonts

⚙️ Scalability: Built on serverless infrastructure with Supabase

🔮 Future Enhancements
🔎 AI job matching with pgvector & embeddings

📱 Mobile version via React Native

🕹️ Gamification: badges, leaderboards

📊 Advanced analytics dashboard

🏢 Enterprise team planning features

🤝 Contributing
We welcome contributions!

bash
Copy
Edit
# Fork the repo
# Create a feature branch
git checkout -b feature/YourFeature

# Commit your changes
git commit -m "Add YourFeature"

# Push the branch
git push origin feature/YourFeature

# Open a Pull Request 🎉
Please follow our Code of Conduct. For issues or suggestions, open a GitHub issue.

📜 License
Licensed under the MIT License.

🙌 Acknowledgements
Supabase

React

React Spring

[Hackathon Organizers] for inspiring this project

📬 Contact
Author: Your Name
GitHub: @yourusername
Email: your.email@example.com
LinkedIn: linkedin.com/in/yourprofile

CareerBoost: Your Career, Your Plan, Your Success! 🌟

python
Copy
Edit

---

Let me know if you'd like me to:
- Add real image links
- Customize contact info
- Include a badge section (e.g. build, license, stars)

I'm happy to help!
