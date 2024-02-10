FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG DATABASE_URL DATABASE_URL="default_values"
ARG OPEN_AI_SECRET_KEY="default_values"
ARG PORT
# Expose the port your FastAPI app will run on
EXPOSE 5432
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]