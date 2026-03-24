FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variable for Python to print output immediately
ENV PYTHONUNBUFFERED=1

# Default command - run Agent_Bot
CMD ["python", "Agents/Agent_Bot.py"]
