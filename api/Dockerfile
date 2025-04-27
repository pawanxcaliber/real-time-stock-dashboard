# Stage 1: Build Stage
# Use a Python base image with a specified version
FROM python:3.12-slim-bullseye as builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
# Use --no-cache-dir and --upgrade pip for clean installs
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Runtime Stage
# Use a smaller base image for the final runtime
FROM python:3.12-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the application code
COPY app.py .
# You might copy more files later if your API grows (e.g., helper modules)
# COPY . . # Be careful with this if you have venv, git, etc.

# Ensure the application runs as a non-root user
# Create a non-root user
RUN adduser --system --group appuser

# Set ownership of the app directory to the new user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application
# Using gunicorn is standard for production Flask apps
# You'll need to add gunicorn to requirements.txt later
# CMD ["gunicorn", "-w", "4", "app:app", "-b", "0.0.0.0:8000"]

# For now, you can use the simple python command if gunicorn is not in requirements
# If you added gunicorn already, use the CMD above. If not, use this one:
CMD ["python", "app.py"]
