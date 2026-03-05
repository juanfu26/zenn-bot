FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

ENV TZ=Europe/Madrid
RUN apt-get update && apt-get install -y tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir pyTelegramBotAPI playwright

# Install only the Chromium browser and its system dependencies
RUN playwright install chromium
RUN playwright install-deps chromium

COPY ./app /app

# Run the script
CMD ["python", "main.py"]