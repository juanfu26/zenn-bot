# Zenn Auto-Clockout Agent (zenn-bot)

A headless automation service designed to run on a **Raspberry Pi** using **Docker**. It allows a user to trigger a smartly delayed clock-out action on the Workday/Zenn HR portal via a **Telegram Bot** simulating realistic human behavior.

## 📚 Documentation
For AI agents and developers, detailed technical documentation can be found in the `docs/` folder:
* [Architecture & Technical Stack (`docs/architecture.md`)](./docs/architecture.md)
* [Business Logic & Commands (`docs/business_logic.md`)](./docs/business_logic.md)
* [AI Agent Guidelines (`AI_INSTRUCTIONS.md`)](./AI_INSTRUCTIONS.md)

---

## ✨ Features
- **Remote Telegram Control:** Start, cancel, or check the status of your auto-clockout without opening router ports.
- **Smart Delays:** Automatically randomized clock-out waits to simulate realistic exit times.
- **Playwright Automation:** Reliable headless browser automation.
- **Security:** Strict IP-less whitelist relying entirely on Telegram User IDs.
- **Cross-Architecture Docker Support:** Fully compatible with ARM devices (`linux/arm64`) like Raspberry Pi, as well as `amd64`.

---

## ⚙️ Configuration
The agent requires the following variables defined in the `compose.yml` (or `.env` file):

| Variable | Description |
| :--- | :--- |
| `TELEGRAM_TOKEN` | Secret API token obtained from [@BotFather](https://t.me/botfather). |
| `TELEGRAM_USER_ID` | Your numeric Telegram ID (Security whitelist). |
| `LOGIN_USER` | Your login email/username for the Zenn portal. |
| `LOGIN_PASS` | Your password. |
| `LOGIN_URL` | Login endpoint. |
| `ACTION_URL` | Attendance action endpoint (e.g., action=389). |

---

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/juanfu26/zenn-bot.git
   cd zenn-bot
   ```

2. Duplicate `.env.example` (or create a new `.env`) and provide your credentials:
   ```env
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_USER_ID=your_id_here
   LOGIN_USER=your_zenn_user
   LOGIN_PASS=your_zenn_pass
   LOGIN_URL=https://your-portal-url.com/login
   ACTION_URL=https://your-portal-url.com/attendance/action=389
   ```

3. Launch via Docker Compose:
   ```bash
   docker compose up -d --build
   ```

### 🛠️ Maintenance & Troubleshooting

**Viewing Logs:**
```bash
docker logs -f zenn-bot
```

**Common Issues:**
* **Selector Timeout:** If the Zenn UI is updated, CSS selectors might need updates.
* **Session Expiry:** Script performs a fresh login every time to avoid session timeout.

---

## 🔄 CI/CD & Docker Hub
This repository uses GitHub Actions to automatically build both `linux/amd64` and `linux/arm64` images and push them to [Docker Hub as `juanfu26/zenn-bot`](https://hub.docker.com/r/juanfu26/zenn-bot). Requires `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets in GitHub.
