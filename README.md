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

# 🌐 Live Deployment

🚀 **Live Demo:**  
https://crisis-sync-ai-five.vercel.app/

The latest deployed version of CrisisSync AI is available online through Vercel.


---

# ✨ Features

## 🚨 Staff Dashboard

- Trigger emergencies
- Select affected floors
- Mark danger zones
- View building status
- Reset emergency
- Monitor live crisis information
- Monitor floor-wise room numbers
- Switch between different hotel floors
- View real-time occupancy information

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
- Floor-wise room numbers
- Occupancy status
- Assembly points
- Live floor switching

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

```text
                    Emergency Trigger
                            │
                            ▼
                     Staff Dashboard
                            │
                            ▼
                 Firebase Realtime Database
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Google Gemini AI     Guest Dashboard    Responder Dashboard
        │                   │                   │
        ▼                   ▼                   ▼
 AI Crisis Analysis   Safe Evacuation    Tactical Briefing
