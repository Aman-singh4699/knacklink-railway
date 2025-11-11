# Use a small Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Set workdir to the Django project folder
WORKDIR /app/employee_dashboard

# 🧠 Prevent collectstatic from breaking at build time
RUN python manage.py collectstatic --noinput || echo "Skipping collectstatic (no DB available yet)"

# Expose Django port
EXPOSE 8000

# Start the Django app
CMD ["gunicorn", "employee_dashboard.wsgi:application", "--bind", "0.0.0.0:8000"]
