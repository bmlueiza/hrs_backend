FROM python:3.11.6

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip

COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver","0.0.0.0:8000"]