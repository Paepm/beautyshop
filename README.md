# Beautyshop – Full-Stack E-Commerce (Portfolio Project)

This is a personal portfolio project: a full-stack e-commerce application built by me (junior developer) in my free time.
Goal: learn and showcase backend development, clean structure, and real-world features (auth, cart, orders, payments).

## Features (high level)
- User registration & login (including email verification)
- Product catalog, cart, orders, checkout flow
- Payments: Stripe & PayPal (webhooks / payment status updates)
- REST APIs for frontend-backend communication
- Docker-based local development setup

## Tech Stack
- Backend: Python, Django, REST APIs
- Frontend: React
- Database: PostgreSQL (dev)
- DevOps: Docker / Docker Compose
- Payments: Stripe, PayPal

## Run locally (basic)
> Note: This repo is for demo/portfolio purposes. Setup can vary depending on your environment.

1. Clone the repository
2. Configure environment variables (use `.env.example` if available)
3. Start the development stack (example):
   - `docker compose -f docker-compose.dev.yml up --build`

Then open:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

## Project Notes
- This project was built without support from other developers.
- Focus was on learning and implementing a clean structure (service layer / modular design) and real payment flows.

## Known Issues / Next Steps
- The project is still under active development and may contain bugs.
- Next steps may include: more tests, UI polish, refactoring, and deployment improvements.

## License
Portfolio / educational project.