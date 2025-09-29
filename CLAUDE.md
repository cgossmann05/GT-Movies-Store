# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based movie store e-commerce application called "GT Movies Store". The project allows users to browse movies, add them to a cart, and make purchases.

## Development Commands

### Running the Development Server
```bash
cd moviesstore
python manage.py runserver
```

### Database Operations
```bash
# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

## Project Architecture

### Django Apps Structure
- **home**: Landing page and about page functionality
- **movies**: Movie catalog, display, and review system
- **accounts**: User authentication and account management
- **cart**: Shopping cart functionality and order processing
- **moviesstore**: Main project configuration and global templates

### Key Models
- `Movie` (movies/models.py): Core movie entity with name, price, description, and image
- `Review` (movies/models.py): User reviews for movies
- `Order` (cart/models.py): Purchase orders containing user and total
- `Item` (cart/models.py): Individual movie items within an order

### URL Routing
Main URL configuration in `moviesstore/urls.py` includes:
- `/admin/` - Django admin interface
- `/` - Home app (landing page)
- `/movies/` - Movie browsing and details
- `/accounts/` - User authentication
- `/cart/` - Shopping cart and checkout

### Template System
- Templates are organized per app in `{app}/templates/` directories
- Global templates in `moviesstore/templates/`
- Static files located in `moviesstore/static/`
- Media files (movie images) stored in `media/` directory

### Key Features
- Session-based shopping cart (stored in `request.session['cart']`)
- User authentication with Django's built-in User model
- Image uploads for movies stored in `media/movie_images/`
- Order processing with item tracking
- Review system for movies

### Database
- Uses SQLite database (`db.sqlite3`) for development
- Django ORM for database operations

## Important Notes

- The project uses Django 5.0
- Static files are configured with `STATICFILES_DIRS` pointing to `moviesstore/static/`
- Media files handling is set up for movie image uploads
- Cart functionality relies on Django sessions
- Authentication is required for purchasing (checkout process)