# Use a slim Python base to keep image size down
FROM python:3.9-slim

# 1. Install system dependencies for the SC2 Linux Engine
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Download & Install SC2 Headless Binary
# The password 'iagreetotheeula' is required by Blizzard
RUN wget http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.10.zip \
    && unzip -P iagreetotheeula SC2.4.10.zip \
    && rm SC2.4.10.zip

#Sym link patch to fix maping
RUN ln -s /StarCraftII/Maps /StarCraftII/maps

# 4. Set up your application code
WORKDIR /StarCraftII
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
COPY ./bots ./bots

CMD ["python", "main.py"]
