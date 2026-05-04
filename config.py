# Copyright (c) 2025 Contributor : https://github.com/Contributor.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import os
import logging
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════════
# ░ CONFIGURATION SETTINGS
# ════════════════════════════════════════════════════════════════════════════════

# VPS --- FILL COOKIES 🍪 in """ ... """ 
INST_COOKIES = """
# write up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

# ─── BOT / DATABASE CONFIG ──────────────────────────────────────────────────────
API_ID       = os.getenv("API_ID", "")
API_HASH     = os.getenv("API_HASH", "")
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")
MONGO_DB     = os.getenv("MONGO_DB", "")
DB_NAME      = os.getenv("DB_NAME", "telegram_downloader")

if not BOT_TOKEN:
    logger.warning("BOT_TOKEN is not set! Please provide a valid bot token from @BotFather.")
if not API_ID or not API_HASH:
    logger.warning("API_ID or API_HASH is not set! Please get them from https://my.telegram.org.")
if not MONGO_DB:
    logger.warning("MONGO_DB is not set! Please provide a valid MongoDB connection string.")

# ─── OWNER / CONTROL SETTINGS ───────────────────────────────────────────────────
OWNER_ID     = list(map(int, os.getenv("OWNER_ID", "").split()))  # space-separated list
STRING       = os.getenv("STRING", None)  # optional session string
LOG_GROUP    = int(os.getenv("LOG_GROUP", "-1001234456"))
PREMIUM_LOGS = int(os.getenv("PREMIUM_LOGS", "-1001234456"))
RENEWAL_REMINDER = os.getenv("RENEWAL_REMINDER", "True").lower() == "true"
FORCE_SUB    = int(os.getenv("FORCE_SUB", "-10012345567"))

# ─── SECURITY KEYS ──────────────────────────────────────────────────────────────
MASTER_KEY   = os.getenv("MASTER_KEY", "gK8HzLfT9QpViJcYeB5wRa3DmN7P2xUq")
IV_KEY       = os.getenv("IV_KEY", "s7Yx5CpVmE3F")

if not os.getenv("MASTER_KEY"):
    logger.warning("MASTER_KEY environment variable is not set, using default value.")
if not os.getenv("IV_KEY"):
    logger.warning("IV_KEY environment variable is not set, using default value.")

# ─── PAYMENT DETAILS ───────────────────────────────────────────────────────────
BANK_DETAILS   = os.getenv("BANK_DETAILS", "")
CRYPTO_ADDRESS = os.getenv("CRYPTO_ADDRESS", "")

# ─── COOKIES HANDLING ───────────────────────────────────────────────────────────
YT_COOKIES   = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)

# ─── USAGE LIMITS ───────────────────────────────────────────────────────────────
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT  = int(os.getenv("PREMIUM_LIMIT", "500"))

# ─── UI / LINKS ─────────────────────────────────────────────────────────────────
JOIN_LINK     = os.getenv("JOIN_LINK", "https://t.me/ModelNorth")
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "https://t.me/ModelNorthSupport")
BOT_NAME      = os.getenv("BOT_NAME", "ModelNorth Bot")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "ModelNorthAdmin")
START_PIC     = os.getenv("START_PIC", "https://graph.org/file/d44f024a08ded19452152.jpg")

# ─── BRANDING SETTINGS ──────────────────────────────────────────────────────────
BRAND_NAME    = os.getenv("BRAND_NAME", "ModelNorth")
SUPPORT_LINK  = os.getenv("SUPPORT_LINK", "https://t.me/ModelNorthSupport")
SUPPORT_CHAT  = os.getenv("SUPPORT_CHAT", SUPPORT_LINK)
CHANNEL_LINK  = os.getenv("CHANNEL_LINK", "https://t.me/ModelNorth")
GROUP_LINK    = os.getenv("GROUP_LINK", SUPPORT_LINK)
BOT_STATS_NAME = os.getenv("BOT_STATS_NAME", "ModelNorthStats")

# ════════════════════════════════════════════════════════════════════════════════
# ░ PREMIUM PLANS CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════════

P0 = {
    "d": {
        "s": int(os.getenv("PLAN_D_S", 1)),
        "du": int(os.getenv("PLAN_D_DU", 1)),
        "u": os.getenv("PLAN_D_U", "days"),
        "l": os.getenv("PLAN_D_L", "Daily"),
    },
    "w": {
        "s": int(os.getenv("PLAN_W_S", 3)),
        "du": int(os.getenv("PLAN_W_DU", 1)),
        "u": os.getenv("PLAN_W_U", "weeks"),
        "l": os.getenv("PLAN_W_L", "Weekly"),
    },
    "m": {
        "s": int(os.getenv("PLAN_M_S", 5)),
        "du": int(os.getenv("PLAN_M_DU", 1)),
        "u": os.getenv("PLAN_M_U", "month"),
        "l": os.getenv("PLAN_M_L", "Monthly"),
    },
}

# ════════════════════════════════════════════════════════════════════════════════
# ░ CONTRIBUTOR
# ════════════════════════════════════════════════════════════════════════════════
