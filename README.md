# 🌌 Nexus | Multi-Tenant SaaS Platform

**Nexus** is a high-performance, enterprise-grade SaaS infrastructure designed for seamless organizational collaboration. Built with a robust **Django/DRF** backend and a reactive, lightweight vanilla JS frontend, it provides a complete foundation for multi-user applications that require real-time synchronization, strict data isolation, and advanced project management tools.

**🔗 Live Demo:** [Nexus on Vercel](https://multi-tenant-saas-project-frontend.vercel.app/)

---

## 🚀 Key Features

### 🏢 Architecture & Security
* **Strict Multi-Tenancy:** Implements row-level isolation at the database level to ensure data is strictly partitioned and secure between different organizations.
* **Intelligent Context Scoping:** The frontend automatically intercepts requests and injects the `X-ORG-SLUG` and `Authorization` headers, ensuring the backend always routes requests to the correct tenant context.
* **JWT Auth with Auto-Refresh:** Secure session management using JSON Web Tokens. Features a background 401-unauthorized interceptor that handles token rotation without interrupting the user's workflow.
* **Organization RBAC:** Granular roles (Owner, Admin, Member, Viewer) with a full email-based invitation system for team onboarding.

### 📝 Real-Time Collaboration
* **Collaborative Note Engine:** Powered by **WebSockets** and **Redis**, allowing multiple users to edit documents simultaneously in real-time.
* **Operational Transformation (OT):** A custom version-based conflict resolution engine ensures document integrity and prevents data loss during concurrent edits.
* **Live Presence & Notifications:** Real-time member online/offline status tracking and live notifications delivered via **SSE (Server-Sent Events)** and **Firebase Cloud Messaging (FCM)** for push alerts.

### 📊 Project & Team Management
* **Kanban Boards:** Dynamic task tracking with drag-and-drop state persistence and status filtering.
* **Workspaces:** Hierarchical containers for organizing boards, notes, and team resources effectively.
* **Subscription & Billing:** Built-in multi-tier subscription logic (Monthly/Yearly) with **PayU** integration for secure payment processing.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Core** | Python, Django, Django Rest Framework (DRF) |
| **Real-Time Engine** | Django Channels, WebSockets, Redis, SSE |
| **Database** | PostgreSQL (with row-level isolation) |
| **Task Queue** | Celery & Redis (Background workers) |
| **Email/Messaging**| Brevo (Transactional Email API), Firebase (FCM) |
| **Frontend** | Vanilla JavaScript (ES6+), CSS3 Variables |
| **Hosting & CI/CD**| Render (API/Redis/DB/Workers), Vercel (Frontend) |

---

## ⚙️ Core Logic Highlights

### Version-Controlled Editing (OT)
The system manages real-time collaboration by tracking document versions to resolve conflicts mathematically:
$$Version_{new} = Version_{base} + Op(Insert | Delete)$$
If two users edit at once, the backend WebSocket consumer resolves the conflict by transforming the operations based on the document's version history, ensuring both edits survive.

### Automated Worker Tasks
Using **Celery** and **Redis**, Nexus offloads heavy, time-consuming operations from the main request-response cycle, including:
* Dispatching organization invites and password reset links via **Brevo**.
* Processing subscription upgrades/downgrades and tracking billing cycles.
* Cleaning up stale user presence heartbeats in the Redis cache.

---

## 📂 Project Structure (Frontend)

* `dashboard.js`: Orchestrates global state, organization switching, sidebar routing, and global data loading.
* `board.js`: Manages the Kanban lifecycle, drag-and-drop events, and task REST API interactions.
* `note.js`: Contains the WebSocket connection logic, Caret (cursor) offset calculation, and OT engine for the collaborative editor.
* `fcm-client.js`: Handles Firebase Service Worker registration and push token synchronization with the backend.
* `login.js` / `signup.js`: Secure authentication flows, dynamic UI state swapping, and backend field-error mapping.
* `payment-success.js` / `payment-failed.js`: Redirection handlers post-PayU transaction.

---

## 🚦 Getting Started (Local Development)

### Prerequisites
* Python 3.10+
* Node.js & npm (for serving the frontend locally, optional)
* PostgreSQL
* Redis Server (Running locally on port 6379)

### 1. Clone the Repository
git clone [https://github.com/yourusername/nexus.git](https://github.com/yourusername/nexus.git)
cd nexus
# Navigate to the backend directory
cd backend

### Backend Setup

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Environment Variables (Create a .env file)
# Required: DATABASE_URL, REDIS_URL, BREVO_API_KEY, PAYU_KEY, SECRET_KEY

# Apply migrations
python manage.py migrate

# Start the development server (ASGI for Channels)
uvicorn -p 8000 config.asgi:application

Start Celery Workers
In a separate terminal (with the virtual environment activated):

celery -A nexus worker -l info
