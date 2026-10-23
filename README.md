# 📄 CV Craft AI — AI-Powered ATS Resume Optimizer

Link: https://cv-craft-ai-mzh9.onrender.com/

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Google_Gemini-API-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Render](https://img.shields.io/badge/Render-Deployment-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

**CV Craft AI** is a full-stack web application built to solve a real-world problem in modern hiring: low resume pass rates caused by **Applicant Tracking Systems (ATS)**.

The platform transforms raw candidate work histories into structured, ATS-compliant resumes in PDF format using AI processing, strategic action verbs, and keyword alignment.

---

## 🛠️ Tech Stack & Architecture

### **Backend**
* **Python**: Core programming language for business logic and integrations.
* **FastAPI**: Asynchronous, high-performance web framework for handling API endpoints.
* **Google Gemini API**: Natural Language Processing (LLM) for professional rewriting, ATS optimization, and contextual translation.
* **ReportLab**: Programmatic PDF document generation adhering to strict ATS formatting guidelines.
* **Zipfile / io**: In-memory compression and archive generation for bilingual dual-pack downloads (`.ZIP`).

### **Frontend**
* **HTML5 & Tailwind CSS**: Modern dark-mode SaaS interface designed using a *vibe coding* workflow.
* **FontAwesome**: Vector icon library for UI elements.
* **Vanilla JavaScript**: Asynchronous DOM manipulation, API fetching, modal management, and clipboard integration.

### **Deployment & Infrastructure**
* **Render**: Cloud hosting for web services and static assets with automated CI/CD deployment linked to GitHub.

---

## 🔥 Key Features

- [x] **ATS-Friendly Formatting**: Clean visual structure with zero graphical clutter to prevent ATS parser errors.
- [x] **AI-Powered Optimization**: Rewrites professional experience bullet points emphasizing measurable achievements and action-oriented verbs.
- [x] **Instant PDF Generation**: Programmatic compilation of downloadable PDF documents in seconds.
- [x] **Bilingual Export (.ZIP)**: Simultaneous export option for resumes in both Portuguese and English within a single workflow.
- [x] **Integrated Support & Donation Modal**: Built-in modal for optional PIX donations featuring QR Code rendering and one-click key copying.
- [x] **Static Institutional Pages**: Dedicated pages for Privacy Policy, Terms of Service, and Support.

---

## 📁 Repository Structure

```text
cv-craft-ai/
├── backend/
│   ├── main.py              # FastAPI app, endpoints, Gemini & ReportLab logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main web application UI
│   ├── privacidade.html     # Privacy Policy static page
│   ├── termos.html          # Terms of Service static page
│   ├── suporte.html         # User Support static page
│   └── qrcode_pix.jpeg      # Static QR Code image for support payments
├── .gitignore               # Ignored files for version control
└── README.md                # Repository documentation
