# Copyright (c) 2025 Contributor : https://github.com/Contributor.
# Licensed under the GNU General Public License v3.0.

import logging
from datetime import timedelta
from config import RENEWAL_REMINDER, ADMIN_CONTACT
from utils.func import get_expiring_users, set_user_reminded

logger = logging.getLogger(__name__)

async def renewal_reminder_job(bot):
    if not RENEWAL_REMINDER:
        return
        
    logger.info("Running renewal reminder job...")
    
    users_to_remind = await get_expiring_users()
    
    for user in users_to_remind:
        user_id = user["user_id"]
        expiry_date = user["subscription_end"]
        expiry_ist = expiry_date + timedelta(hours=5, minutes=30)
        formatted_expiry = expiry_ist.strftime('%d-%b-%Y %I:%M:%S %p')
        
        message = (
            f"⚡️ **Premium Renewal Reminder** ⚡️\n\n"
            f"Your premium subscription is expiring soon (in about 24 hours)!\n"
            f"**Expiry Time**: {formatted_expiry} (IST)\n\n"
            f"To continue using premium features without interruption, please renew your subscription.\n"
            f"Contact: {ADMIN_CONTACT}"
        )
        
        try:
            # The bot passed here is the Pyrogram client from main.py
            await bot.send_message(user_id, message)
            await set_user_reminded(user_id)
            logger.info(f"Sent 24h renewal reminder to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send renewal reminder to {user_id}: {e}")
