# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-powered customer support ticket triaging system for "Acme Rentals", a cabin rental marketplace. The system uses machine learning to automatically categorize and suggest solutions for customer support tickets, achieving >95% accuracy in ticket categorization.

## Development Commands

### Frontend (Next.js)
- **Install dependencies**: `cd frontend && npm install`
- **Development server**: `npm run dev` (runs on http://localhost:3000)
- **Build**: `npm run build`
- **Production server**: `npm start`
- **Linting**: `npm run lint`

### Backend (FastAPI)
- **Install dependencies**: `cd backend && pip install -e .`
- **Run server**: `python -m src.main` (runs on http://localhost:8000)
- **API docs**: Available at http://localhost:8000/docs when server is running

### Data Service
- **Install dependencies**: `cd data && pip install -r requirements.txt`

## Architecture Overview

### Monorepo Structure
- `frontend/`: Next.js 15 + React 19 web application
- `backend/`: Python FastAPI service with AI integration
- `data/`: Data processing service for AWS integration
- `docs-and-mock-data/`: Documentation and mock datasets for training

### Technology Stack

**Frontend**:
- Next.js 15 with App Router
- shadcn/ui component library
- Tailwind CSS for styling
- React Hook Form + Zod for form validation
- TypeScript for type safety

**Backend**:
- FastAPI (Python) for REST API
- Weaviate vector database for semantic search
- OpenAI API for AI-powered categorization
- Pydantic for data validation

### Key Features

1. **Ticket Management**
   - Dashboard with filtering, sorting, and search
   - Five main problem categories:
     - Booking & Reservation Issues
     - Payment & Billing Issues
     - Property & Stay Issues
     - Host/Seller Issues
     - Technical & App Issues

2. **AI Integration**
   - Weaviate vector database stores ticket embeddings
   - OpenAI API generates embeddings and suggestions
   - Semantic search for finding similar issues

3. **Admin Features**
   - Category management interface
   - Analytics dashboard (placeholder)
   - Documentation management

### API Integration

The frontend communicates with the backend via REST API:
- Base URL: `http://localhost:8000`
- Main endpoints:
  - `GET /tickets`: Fetch all tickets
  - `POST /tickets`: Create new ticket
  - `GET /tickets/{id}`: Get ticket details
  - `PUT /tickets/{id}`: Update ticket
  - `POST /categorize`: AI-powered categorization

### Environment Configuration

**Backend (.env)**:
```
OPENAI_API_KEY=your-api-key-here
WEAVIATE_URL=http://localhost:8080
```

### Mock Data Structure

The `docs-and-mock-data/` directory contains:
- `mock_issues_dataset.csv`: Sample customer issues with categories and solutions
- Category-specific FAQ documents
- Company policies and documentation

Each mock issue includes:
- Problem description
- Category
- Suggested solution
- Customer sentiment
- Resolution time estimates