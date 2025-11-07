# EcoVerse — Multi-Agent Environmental Monitoring & Action System

## Overview
EcoVerse is a multi-agent AI system designed for real-time environmental monitoring, analysis, and automated eco-action. 
It integrates sensing, analysis, alerting, and coordination agents for sustainable ecosystem intelligence.

## Key Modules
- **Agents**: Independent modules for sensing, analysis, and action.
- **Core**: System orchestration and task scheduling.
- **Models**: ML and AI models for prediction and analysis.
- **Interfaces**: REST API, Dashboard, and CLI.
- **Pipelines**: Data and workflow automation.
- **Deployment**: Containerization and orchestration files.

## Run
Step 1: Clone and Setup
```
# Clone repository
git clone https://github.com/Arvind-55555/EcoVerse_Multi-Agent_AI_for_Environmental_Monitoring.git
cd EcoVerse_Multi-Agent_AI_for_Environmental_Monitoring

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```
Step 2: Configuration
```
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```
Step 3: Database Setup
```
# Start PostgreSQL and Redis with Docker
docker-compose up -d postgres redis

# Run database migrations
python -m alembic upgrade head

# Or use Docker
docker-compose exec ecoverse-api python -m alembic upgrade head
```
Step 4: Start Services
```
# Option 1: Docker Compose (Recommended)
docker-compose up -d

# Option 2: Manual Start
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - Agents
python -m src.agents.implementations
```
Step 5: Access Applications
```
Dashboard: http://localhost:3000
API Docs: http://localhost:8000/api/docs
Prometheus: http://localhost:9090
Grafana: http://localhost:3001 (admin/admin_password)
```

## License
MIT License
    
