#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Generate images if they don't exist (helpful when volumes are used)
echo "Generating placeholder images"
python generate_images.py

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
