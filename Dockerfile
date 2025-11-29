# ---- BASE IMAGE ----
FROM python:3.11-slim

# ---- SYSTEM UPDATES & INSTALLS ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---- WORK DIRECTORY ----
WORKDIR /app

# ---- COPY REQUIREMENTS ----
COPY requirements.txt .

# ---- INSTALL PYTHON PACKAGES ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- COPY PROJECT FILES ----
COPY . .

# ---- ENV FILE ----
# .env faylni konteyner ichiga o'tkazamiz
COPY .env /app/.env

# ---- RUN BOT ----
CMD ["python3", "bot.py"]
