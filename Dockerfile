# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set working directory to the Django project
WORKDIR /app/employee_dashboard

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Start Django with Gunicorn (for Railway)
CMD ["gunicorn", "employee_dashboard.wsgi:application", "--bind", "0.0.0.0:8000"]
