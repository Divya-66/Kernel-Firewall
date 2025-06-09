CareerBoost 🚀
 
A comprehensive career development platform empowering users to plan, track, and achieve their professional goals with AI-driven insights, real-time mentorship, and a polished user experience.

📖 About CareerBoost
CareerBoost is an all-in-one web application designed to streamline career advancement for students, early-career professionals, and career switchers. By integrating personalized job recommendations, skill development, professional branding, and community support, CareerBoost transforms the fragmented career journey into a unified, engaging experience. Built with React, Supabase, and PostgreSQL, it delivers a scalable, cloud-based solution with a sleek, modern interface.
Key Features

Interactive Career Roadmap: Visualize your journey with a dynamic timeline of completed courses, goals, and job applications.
Skill Mastery Dashboard: Track skill proficiency with animated radial progress bars, identifying gaps for targeted growth.
AI-Powered Job Recommendations: Get tailored job listings based on your skills and goals.
Learning Paths: Curate courses aligned with career aspirations, synced to your profile and resume.
Resume & Portfolio Builder: Generate professional PDF resumes and showcase projects with shareable links.
Task & Goal Tracking: Set career milestones, break them into tasks, and monitor progress with visual feedback.
Mock Interview Simulator: Practice common interview questions with AI-generated feedback.
Real-Time Mentorship Chat: Connect with mentors for live guidance and peer collaboration.
Community Forum: Share insights, ask questions, and engage with a supportive career network.
Analytics & Contests: Monitor progress with stats and compete in skill-based challenges for motivation.


🎯 Problem Statement
In today’s competitive job market, career development is fragmented across disconnected tools—job boards, MOOCs, resume templates, and networking platforms. This leads to inefficiencies, skill gaps, lack of professional polish, and isolation. CareerBoost solves this by providing a unified platform that:

Guides users with a clear career roadmap.
Bridges skill gaps with personalized recommendations.
Enhances employability through professional outputs.
Fosters community via mentorship and forums.
Motivates action with analytics and gamification.


🛠️ Tech Stack



Category
Technology



Frontend
React, Tailwind CSS, React Spring, React Circular Progressbar


Backend
Supabase (PostgreSQL, PostgREST, Supavisor)


Database
PostgreSQL (with RLS, JSONB, Triggers)


Real-Time
Supabase WebSockets, Socket.IO (Mentorship Chat)


File Storage
Supabase Storage (S3-compatible)


Authentication
Supabase Auth (JWT, Email, OAuth)


PDF Generation
jsPDF (Resumes, Portfolios)


Deployment
Vercel (Frontend), Supabase Cloud (Backend)



🖼️ Screenshots



Dashboard
Skill Mastery










Portfolio
Mentorship Chat










🚀 Getting Started
Prerequisites

Node.js (v16 or higher)
Supabase account (Sign up)
GitHub account for cloning the repository

Installation

Clone the Repository:
git clone https://github.com/yourusername/careerboost.git
cd careerboost


Install Dependencies:
npm install


Set Up Supabase:

Create a new project in the Supabase Dashboard.
Copy your Project URL and Anon Key from the API settings.
Create a .env file in the project root:REACT_APP_SUPABASE_URL=your-supabase-url
REACT_APP_SUPABASE_ANON_KEY=your-anon-key




Initialize Database:

Run the SQL scripts in database/setup.sql via Supabase’s SQL Editor to create tables (profiles, jobs, portfolio, etc.) and enable RLS.
Example:CREATE TABLE profiles (
  id UUID PRIMARY KEY,
  email TEXT,
  skills TEXT[] DEFAULT '{}',
  skill_mastery JSONB DEFAULT '[]'
);
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;




Start the Application:
npm start

Open http://localhost:3000 in your browser.

Optional: Real-Time Chat Server:

For mentorship chat, set up a mock Socket.IO server:npm install -g json-server
json-server --watch db.json --port 3001






📂 Project Structure
careerboost/
├── public/
│   ├── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js
│   │   ├── SkillMastery.js
│   │   ├── Portfolio.js
│   │   ├── People.js
│   │   ├── ... (other components)
│   ├── styles/
│   │   ├── styles.css
│   │   ├── SkillMastery.css
│   │   ├── Portfolio.css
│   ├── supabaseClient.js
│   ├── App.js
├── database/
│   ├── setup.sql
├── .env
├── README.md
├── package.json


🔧 Usage

Sign Up/Login: Create an account using email or OAuth to access the dashboard.
Set Goals: Define career goals (e.g., "Become a Web Developer") and break them into tasks.
Explore Jobs: View AI-driven job recommendations tailored to your skills.
Learn & Track: Enroll in courses, track skill mastery, and update your profile.
Build Assets: Generate a PDF resume and add projects to your portfolio.
Practice Interviews: Use the mock interview simulator with AI feedback.
Connect: Chat with mentors or post in the forum for community insights.
Monitor Progress: Check your career roadmap and analytics for motivation.


🌟 Hackathon Highlights

Innovation: Combines AI-driven personalization, real-time collaboration, and dynamic visualizations in one platform.
Impact: Empowers users to overcome career barriers with actionable tools and community support.
Polish: Features a professional UI with smooth animations (React Spring), modern fonts (Inter, Roboto), and responsive design.
Scalability: Leverages Supabase’s serverless PostgreSQL and WebSockets for robust performance.


🔮 Future Enhancements

AI Job Matching: Integrate pgvector for semantic job-skill matching.
Mobile App: Develop a React Native version for iOS/Android.
Gamification: Add badges and leaderboards for contests.
Analytics Dashboard: Deepen insights with predictive career trends.
Enterprise Integration: Support team-based career planning for organizations.


🤝 Contributing
Contributions are welcome! To get started:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m 'Add YourFeature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request with a clear description.

Please follow the Code of Conduct and report issues via GitHub Issues.

📜 License
This project is licensed under the MIT License.

🙌 Acknowledgements

Supabase for an amazing BaaS platform.
React for a robust frontend framework.
React Spring for smooth animations.
[Hackathon Organizers] for inspiring this project!


📬 Contact

Author: Your Name
GitHub: yourusername
Email: your.email@example.com
LinkedIn: Your LinkedIn

Feel free to reach out for collaboration or feedback!

CareerBoost: Your Career, Your Plan, Your Success! 🌟
