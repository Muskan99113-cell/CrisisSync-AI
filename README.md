# 🚨 CrisisSync AI

<p align="center">
  <h2 align="center">AI-Powered Crisis Management & Emergency Response System</h2>

  <p align="center">
    Built using <b>Flask</b> • <b>Google Gemini AI</b> • <b>Firebase Realtime Database</b>
  </p>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-blue?logo=google)
![Firebase](https://img.shields.io/badge/Firebase-Realtime_Database-orange?logo=firebase)
![Status](https://img.shields.io/badge/Status-Working-success)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 📖 Overview

**CrisisSync AI** is an intelligent emergency response platform designed to improve safety and coordination during critical situations inside hotels, hospitals, campuses, offices, and other large facilities.

Traditional evacuation systems rely on predefined emergency plans that cannot adapt to changing conditions. CrisisSync AI addresses this limitation by combining **Google Gemini AI** with **Firebase Realtime Database** to provide dynamic evacuation guidance, AI-assisted responder briefings, and synchronized real-time crisis monitoring.

The platform enables staff to declare emergencies, guests to receive personalized evacuation instructions, and responders to access AI-generated rescue strategies, all from a single integrated system.

---

# 🎯 Problem Statement

During emergencies such as fires, gas leaks, or other hazards:

- Guests often do not know the safest evacuation route.
- Emergency responders receive limited situational information.
- Staff members struggle to coordinate rescue operations efficiently.
- Static evacuation plans cannot adapt to changing danger zones.

These limitations increase evacuation time and reduce overall emergency response efficiency.

---

# 💡 Proposed Solution

CrisisSync AI provides a centralized AI-powered crisis management platform where:

- Staff members can trigger an emergency instantly.
- Google Gemini AI analyzes the crisis.
- Firebase synchronizes information in real time.
- Guests receive personalized evacuation routes.
- Emergency responders receive AI-generated tactical briefings.
- Administrators monitor the complete situation through a live dashboard.

---

# 🎥 Project Demonstration

📹 **Project Demo Video**

https://drive.google.com/file/d/1Aka3lm9y9_eSCoMQL2QJ_1QToGPoDLWV/view

---

# ✨ Features

## 🚨 Staff Dashboard

- Trigger emergencies
- Select affected floors
- Mark danger zones
- View building status
- Reset emergency
- Monitor live crisis information

---

## 🤖 AI-Powered Crisis Analysis

Google Gemini AI generates:

- Emergency severity
- Immediate actions
- Evacuation recommendations
- Estimated evacuation time
- Risk assessment

---

## 🗺 Live Floor Monitoring

The dashboard displays:

- Safe zones
- Danger zones
- Floor information
- Occupancy status
- Assembly points

---

## 👥 BLE-Based Occupant Tracking

Track occupants using BLE tags including:

- Guest location
- Room number
- Current floor
- User role
- Special assistance requirements

---

## 🧭 Personalized Guest Evacuation

Guests receive:

- AI-generated evacuation routes
- Safe exit guidance
- Dynamic route updates
- Personalized instructions

---

## 🚒 Emergency Responder Dashboard

Provides responders with:

- AI-generated tactical briefing
- High-risk locations
- Rescue priorities
- Recommended entry points
- Operational guidance

---

## 🔄 Real-Time Synchronization

Firebase Realtime Database keeps:

- Staff Dashboard
- Guest Dashboard
- Responder Dashboard

fully synchronized throughout the emergency.

---

## 🔁 Crisis Reset

After the emergency is resolved, administrators can reset the complete system using a single action.

---

# 🏗️ System Architecture

```
                    Emergency Trigger
                            │
                            ▼
                     Staff Dashboard
                            │
                            ▼
              Firebase Realtime Database
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
   Google Gemini AI    Guest Dashboard   Responder Dashboard
         │                  │                  │
         ▼                  ▼                  ▼
 AI Crisis Analysis   Safe Evacuation     Tactical Briefing
```

---

# 🔄 System Workflow

### Step 1

Staff member declares an emergency.

↓

### Step 2

Emergency information is stored in Firebase.

↓

### Step 3

Google Gemini AI analyzes the emergency.

↓

### Step 4

The system identifies:

- Severity
- Danger zones
- Safe evacuation routes
- Immediate actions

↓

### Step 5

Guests receive personalized evacuation guidance.

↓

### Step 6

Emergency responders receive AI-generated tactical instructions.

↓

### Step 7

Administrators monitor the crisis in real time.

↓

### Step 8

Once resolved, the system is reset.

---

# 💻 Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend Development |
| Flask | Web Framework |
| Google Gemini AI | AI Decision Making |
| Firebase Realtime Database | Real-Time Cloud Database |
| HTML5 | Frontend |
| CSS3 | Styling |
| JavaScript | Interactive UI |
| REST API | Communication |

---

# 📂 Project Structure

```
CrisisSync-AI/

│── app.py
│── firebase_config.py
│── gemini_service.py
│── requirements.txt
│── .env

├── templates
│   ├── staff.html
│   ├── guest.html
│   └── responder.html

├── static
│   ├── css
│   ├── js
│   └── images

└── README.md
```

---





## 🤖 AI Crisis Analysis Dashboards
<img width="1402" height="1122" alt="image" src="https://github.com/user-attachments/assets/08a4ccb4-c354-4e27-ac91-b7f19745b6d3" />



# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/Muskan99113-cell/CrisisSync-AI.git
```

### Move into the project

```bash
cd CrisisSync-AI
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add:

- Google Gemini API Key
- Firebase Credentials

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 📈 Future Enhancements

- 📱 Android & iOS application
- 📍 Indoor navigation
- 📡 GPS integration
- 📢 SMS emergency alerts
- 📧 Email notifications
- 🔔 Push notifications
- 🎙 Voice-guided evacuation
- 📷 CCTV-assisted hazard detection
- 🌐 Multi-building support
- 📊 Predictive AI risk analysis

---

# 🌟 Project Highlights

- 🤖 AI-Powered Emergency Analysis
- 🚨 Dynamic Crisis Management
- 🗺 Intelligent Evacuation Routes
- 🔄 Real-Time Firebase Synchronization
- 🚒 AI Tactical Briefings
- 👥 BLE Occupant Tracking
- ☁ Cloud-Based Architecture
- ⚡ Fast Emergency Response







### LinkedIn

 https://www.linkedin.com/in/muskan-sharma-4a32b9333/ 

