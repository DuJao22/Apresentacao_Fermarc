# Fermarc Robótica - E-commerce Platform

## Overview
Full-featured e-commerce platform for Fermarc Robótica, a Brazilian robotics and electronics components store. Built with Python/Flask, the system includes complete user authentication, shopping cart, checkout, admin dashboard, and product management.

## Project Structure
- `app/` - Main Flask application
  - `routes/` - Route handlers (public, auth, cart, admin, api)
  - `templates/` - Jinja2 HTML templates
  - `static/` - CSS, JavaScript, images
  - `models.py` - SQLAlchemy database models
  - `forms.py` - WTForms form definitions
  - `utils.py` - Utility functions
  - `config.py` - Application configuration
- `migrations/` - Alembic database migrations
- `run.py` - Application entry point
- `README.md` - Project documentation

## Technology Stack
**Backend:**
- Python 3.11+ with Flask 3.0
- SQLAlchemy ORM
- Flask-Migrate for database migrations
- Flask-Login for authentication
- Flask-WTF for forms and CSRF protection
- Flask-Limiter for rate limiting

**Frontend:**
- Bootstrap 5 for responsive design
- Font Awesome 6 for icons
- Jinja2 templates
- Vanilla JavaScript

**Database:**
- PostgreSQL (production/Replit)
- SQLite (local development fallback)

## Recent Changes (October 30, 2025)
- **Bug Fix:** Initialized database with migrations and seed data
- Created all database tables (users, products, categories, orders, coupons, etc.)
- Seeded database with sample products, categories, and admin account
- Verified app is running correctly without errors

## Features
**For Customers:**
- User registration and authentication
- Advanced product search with filters
- Persistent shopping cart
- Complete checkout system with address management
- Order history and tracking
- Coupon/discount system
- Dynamic shipping calculation

**For Administrators:**
- Dashboard with real-time metrics
- Product, category, and coupon management (CRUD)
- Order management and status updates
- Image upload for products
- CSV import/export
- Sales reports

**SEO & Marketing:**
- SEO-friendly URLs (slugs)
- Dynamic meta tags
- Automatic sitemap.xml generation

## Database Access
**Admin Account:**
- Email: admin@fermarc.com.br
- Password: admin123
- Access: /admin

**Test User Account:**
- Email: cliente@example.com
- Password: cliente123

**Sample Coupons:**
- BEMVINDO10 - 10% off on purchases over R$100
- FRETE20 - R$20 off on purchases over R$150

## User Preferences
None documented yet.

## Project Architecture
Flask MVC architecture with blueprints:
- **Models:** SQLAlchemy ORM for data layer
- **Views:** Jinja2 templates for presentation
- **Controllers:** Flask blueprints for route organization
- **Security:** CSRF protection, password hashing, rate limiting, secure sessions
- **Database:** PostgreSQL with Alembic migrations

## Known Issues
- Email system is simulated (prints to console instead of sending emails)
- Password reset functionality is incomplete (marked as development)
- Production SECRET_KEY should be set via environment variable
