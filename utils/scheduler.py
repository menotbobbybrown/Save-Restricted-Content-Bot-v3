# Copyright (c) 2025 Contributor : https://github.com/Contributor.
# Licensed under the GNU General Public License v3.0.

import logging
from datetime import datetime, timedelta
from config import RENEWAL_REMINDER, ADMIN_CONTACT
from utils.func import premium_users_collection

logger = logging.getLogger(__name__)

async def renewal_reminder_job(bot):
    if not RENEWAL_REMINDER:
        return
        
    logger.info("Running renewal reminder job...")
    
    now = datetime.now()
    reminder_window = now + timedelta(hours=24)
    
    # Query users with subscription_end between now and now + 24 hours where reminder_sent is not True
    cursor = premium_users_collection.find({
        "subscription_end": {"$gt": now, "$lt": reminder_window},
        "reminder_sent": {"$ne": True}
    })
    
    users_to_remind = await cursor.to_list(length=None)
    
    for user in users_to_remind:
        user_id = user["user_id"]
        expiry_date = user["subscription_end"]
        expiry_ist = expiry_date + timedelta(hours=5, minutes=30)
        formatted_expiry = expiry_ist.strftime('%d-%b-%Y %I:%M:%S %p')
        
        message = (
            f"⚡️ **Premium Renewal Reminder** ⚡️\n\n"
            f"Your premium subscription is expiring soon!\n"
            f"**Expiry Time**: {formatted_expiry} (IST)\n\n"
            f"To continue using premium features without interruption, please renew your subscription.\n"
            f"Contact: {ADMIN_CONTACT}"
        )
        
        try:
            await bot.send_message(user_id, message)
            await premium_users_collection.update_one(
                {"user_id": user_id},
                {"$set": {"reminder_sent": True}}
            )
            logger.info(f"Sent renewal reminder to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send renewal reminder to {user_id}: {e}")
