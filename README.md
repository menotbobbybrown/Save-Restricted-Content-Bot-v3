# 🚀 Premium Save Restricted Content Bot

A powerful Telegram bot designed to save restricted content from channels and groups, with advanced features like batch processing, YouTube/social media downloading, and premium membership management.

## ✨ Features

- **Save Restricted Content**: Extract posts from channels or groups where forwarding and saving are disabled.
- **Bulk Extraction**: Process multiple messages at once using the `/batch` command.
- **Media Downloader**: Download videos and audio from YouTube, Instagram, and other social platforms using `/dl` and `/adl`.
- **Session Login**: Support for both bot token and user session string for private channel access.
- **Premium Management**:
    - Multi-tier premium plans.
    - Automated 24-hour renewal reminders via APScheduler.
    - Owner commands for managing subscriptions (`/add`, `/revoke`, `/extend`, `/status`, `/getall`).
- **Custom Branding**: Fully customizable branding via environment variables.
- **Web Interface**: Simple Flask-based web interface for monitoring bot status.

## 🛠️ Prerequisites

- Python 3.10 or higher.
- MongoDB database.
- Telegram API ID and API Hash.
- Bot token from @BotFather.

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_ID` | Your Telegram API ID | Required |
| `API_HASH` | Your Telegram API Hash | Required |
| `BOT_TOKEN` | Your Telegram Bot Token | Required |
| `MONGO_DB` | MongoDB Connection URI | Required |
| `OWNER_ID` | space-separated list of Owner IDs | Required |
| `BRAND_NAME` | Branding name for the bot | Premium Bot |
| `BOT_NAME` | Name of the bot | Save Restricted Bot |
| `OWNER_USERNAME`| Username of the admin | admin |
| `SUPPORT_CHAT` | Link to support group | - |
| `JOIN_LINK` | Link to your Telegram channel | - |
| `ADMIN_CONTACT` | Link to contact admin | - |
| `START_PIC` | URL for the bot's start image | - |
| `FORCE_SUB` | ID of channel for force subscription | - |
| `LOG_GROUP` | ID of the log group | - |
| `PREMIUM_LOGS` | ID of the group for premium logs | - |

## 🚀 Installation

### Manual Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/save-restricted-bot.git
   cd save-restricted-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file or export the variables listed above.

4. **Run the bot**:
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t save-restricted-bot .
   ```

2. **Run the container**:
   ```bash
   docker run -d --env-file .env save-restricted-bot
   ```

## 📜 Commands

### Owner Commands (Restricted to OWNER_ID)
- `/add <user_id> <value> <unit>`: Add premium subscription.
- `/revoke <user_id>`: Remove premium subscription.
- `/extend <user_id> <value> <unit>`: Extend existing subscription.
- `/status <user_id>`: Check subscription status of any user.
- `/getall`: List all active premium users.
- `/set`: Configure bot commands menu.

### User Commands (Private Only)
- `/start`: Start the bot and see welcome message.
- `/help`: Show help menu with feature details.
- `/plans`: View available premium plans.
- `/myplan`: Check your subscription details.
- `/paid`: Instructions for purchasing premium.
- `/login`: Log into private channels.
- `/logout`: Logout from the bot.
- `/batch`: Start bulk extraction.
- `/dl <link>`: Download video from social media.
- `/adl <link>`: Download audio from social media.
- `/settings`: Personalize bot settings.
- `/cancel`: Cancel ongoing process.

## ⚖️ License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
