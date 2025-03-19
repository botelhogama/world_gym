# 🏋️‍♂️ World Gym

```markdown
# 📌 About the Project

World Gym is a fitness-oriented application designed to enhance gym operations by providing 
management insights, optimizing equipment and space usage, and improving client engagement.

This repository contains the backend logic, frontend components, and database integration for 
managing gym clients and predicting churn.

## 🔥 Objectives:
- 📊 Gym occupancy monitoring
- 🏋️ Equipment usage tracking
- 🔄 Client frequency control
- 🎯 Marketing efficiency analysis
- 📈 Other key management metrics

This model is built using Python and Scikit-Learn, incorporating feature engineering techniques such as 
calculating the distance between clients' homes and gyms along with other transformations.

---

# 🎯 Features

✅ **API Integration** – Structured API for data handling and frontend-backend communication.  
✅ **Client Location Processing** – Calculate the distance from clients' homes to gyms.  
✅ **Churn Prediction Model** – Use Scikit-Learn to estimate the probability of client churn.  
✅ **Occupancy & Equipment Usage Monitoring** – Track real-time usage of gym spaces and equipment.  
✅ **Marketing Efficiency Analysis** – Evaluate marketing campaigns' impact on gym attendance and retention.  

---

# 📂 Repository Structure

📂 world_gym/  
├── 📂 backend/            # Backend logic and API services  
│   ├── app.py            # Main application entry point  
│   ├── database.py       # Database connections and models  
│   ├── routes/           # API routes for users and management  
│   ├── models.py         # Data models for clients and usage tracking  
│   ├── churn_model.py    # Churn prediction model implementation  
│   ├── feature_engineering.py  # Distance calculation and data transformation  
│   └── requirements.txt  # Dependencies for the backend  
│  
├── 📂 frontend/           # Frontend components and UI  
│   ├── src/              # Source files for the UI  
│   ├── public/           # Public assets (e.g., images, icons)  
│   ├── index.html        # Main entry point for the frontend  
│   └── package.json      # Frontend dependencies  
│  
├── 📂 data/               # Data files for model training and analysis  
│   ├── raw_data.csv      # Raw client and gym data  
│   ├── processed_data.csv # Data after feature engineering  
│   ├── model.pkl         # Saved trained churn model  
│   └── distance_data.csv # Processed distances from clients to gyms  
│  
├── 📜 README.md          # Project documentation (this file)  
└── 📜 .gitignore         # Git ignore rules  

---

## 🚀 Installation Guide

1️⃣ Clone the Repository  
```bash
git clone https://github.com/botelhogama/world_gym.git
cd world_gym
2️⃣ Backend Setup

📥 Install dependencies:

bash
Copy
Edit
cd backend
pip install -r requirements.txt
🚀 Run the backend server:

bash
Copy
Edit
python app.py
3️⃣ Frontend Setup

📥 Install dependencies:

bash
Copy
Edit
cd frontend
npm install
🚀 Start the frontend server:

bash
Copy
Edit
npm start
📊 API Endpoints
Method	Endpoint	Description
GET	/api/clients	Fetch all client data
POST	/api/clients	Add new client data
GET	/api/churn	Get churn probability for a client
GET	/api/occupancy	Get real-time gym space and equipment usage
GET	/api/marketing	Analyze marketing campaign effectiveness
📈 Churn Prediction Model
The churn prediction model uses Scikit-Learn to analyze client data and estimate their probability of churn.

🔹 Feature Engineering Includes:
📏 Distance Calculation – Measuring the proximity of clients to the nearest gym.
📊 Activity Tracking – Monitoring gym attendance and workout patterns.
📅 Subscription Details – Evaluating membership duration and renewal history.
📢 Marketing Engagement – Assessing how marketing efforts impact client retention.
🏋️ Space & Equipment Utilization – Identifying gym usage trends for better resource allocation.

🏃 Running the Churn Prediction Model

bash
Copy
Edit
cd backend
python churn_model.py
