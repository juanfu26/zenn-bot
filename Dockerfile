FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# No need to install tzdata, we use environment variables for time.
# We keep basic structure for app execution.

WORKDIR /app

RUN pip install --no-cache-dir pyTelegramBotAPI playwright

# Install only the Chromium browser and its system dependencies
RUN playwright install chromium
RUN playwright install-deps chromium

COPY ./app /app

# Run the script
CMD ["python", "main.py"]