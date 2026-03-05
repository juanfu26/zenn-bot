# System Architecture and Execution Flow

This document outlines the technical design of the Zenn Auto-Clockout Agent.

## 🏗️ System Architecture

The system consists of three main layers:
1.  **Interface Layer (Telegram):** Acts as the remote control. No ports need to be opened on your router, as the bot uses long-polling to fetch messages.
2.  **Logic Layer (Python/Threading):** Handles the sign-out countdown using Python's `threading` module to remain responsive while waiting. The duration is calculated dynamically based on the current date (Standard, Friday, or Summer schedules).
3.  **Automation Layer (Playwright):** A headless Chromium instance that handles the authentication and the DOM interaction with the Odoo-based Zenn portal.

---

## 🛠️ Technical Stack

* **Runtime:** Python 3.10+
* **Automation:** Playwright (Chromium)
* **Communication:** `pyTelegramBotAPI` (Telebot)
* **Containerization:** Docker & Docker Compose
* **Target Hardware:** Raspberry Pi (ARM64 / ARMv7)

---

## 🚀 Execution Flow

1.  **Start:** Upon container boot, the bot sends a "System Online" message to the configured `USER_ID`.
2.  **Trigger:** User sends the `/start` command via Telegram.
3.  **Wait:** The system calculates a dynamic delay based on environment configuration and the current date:
    * **Summer Period:** `WORK_MINUTES_SUMMER` + Random.
    * **Friday:** `WORK_MINUTES_FRIDAY` + Random.
    * **Monday-Thursday:** `WORK_MINUTES_REGULAR` + `WORK_MINUTES_LUNCH` + Random.
    *(Refer to RN-10 for details)*.
4.  **Action:** 
    * Initializes a Headless Chromium instance.
    * Navigates to the Zenn Login page.
    * Injects credentials and authenticates.
    * Navigates directly to the Attendance Action URL (`action=389`).
    * Locates and clicks the specific Sign-Out icon: `<i class="fa-sign-out... ">`.
5.  **Notification:** User receives a Telegram confirmation message once the operation is successful or an error report if it fails.
