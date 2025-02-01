# GameTracker

GameTracker is a modern web application that helps gamers track their gaming progress, discover new games, and manage their gaming collections. Built with a modern tech stack combining Vue.js for the frontend and FastAPI for the backend, along with multiple databases for different functionalities.

## 🚀 Features

- Search and discover games using the IGDB API
- Track favorite games
- User authentication and profiles
- Responsive design for all devices
- Real-time game search
- Personal game collection management

## 🛠️ Technology Stack

### Frontend
- **Vue.js 3**: Latest version with Composition API
- **Pinia**: State management
- **Vue Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library
- **Axios**: HTTP client

### Backend
- **FastAPI**: Modern, fast Python web framework
- **Uvicorn**: ASGI server
- **Python 3.11+**: Latest stable version

### Databases
- **MySQL**: Primary database for user data
- **MongoDB**: Game likes and collections
- **Neo4j**: (Prepared for future social features)

### External APIs
- **IGDB API**: Game data and information

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 🏗️ Architecture

The application follows a microservices-inspired architecture with:
- Frontend container (Vue.js)
- Backend container (FastAPI)
- Database containers (MySQL, MongoDB, Neo4j)
- Nginx reverse proxy

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js (for local development)
- Python 3.11+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gametracker.git
cd gametracker
```

2. Create necessary environment files:
```bash
cp .env.example .env
```

3. Start the application using Docker Compose:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost:3535
- Backend API: http://localhost:5050
- PHPMyAdmin: http://localhost:8080

### Local Development

For frontend development:
```bash
cd frontend
npm install
npm run dev
```

For backend development:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📚 API Documentation

**soon**

## 🔐 Security

- Passwords are hashed using bcrypt
- CORS protection enabled
- Environment variables for sensitive data
- Token-based authentication

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a pull request

