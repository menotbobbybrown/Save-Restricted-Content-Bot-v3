# Copyright (c) 2025 Contributor : https://github.com/Contributor.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import client as bot_client, app
from telethon import events
from datetime import datetime, timedelta
from config import OWNER_ID, PREMIUM_LOGS, P0, CHANNEL_LINK as JL, SUPPORT_LINK as AC, OWNER_USERNAME, BOT_NAME, START_PIC, BRAND_NAME
from utils.func import (
    add_premium_user, 
    is_private_chat, 
    get_premium_details, 
    get_all_premium_users, 
    premium_users_collection, 
    is_premium_user, 
    get_display_name,
    revoke_premium_user,
    extend_premium_user
)
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as IK, InlineKeyboardMarkup as IKM
from plugins.start import subscribe


@bot_client.on(events.NewMessage(pattern='/add'))
async def add_premium_handler(event):
    if not await is_private_chat(event):
        return
    
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        return
        
    text = event.message.text.strip()
    parts = text.split(' ')
    if len(parts) != 4:
        await event.respond("Invalid format. Use: `/add user_id duration_value duration_unit` \nExample: `/add 123456 1 weeks`")
        return
        
    try:
        target_user_id = int(parts[1])
        duration_value = int(parts[2])
        duration_unit = parts[3].lower()
        valid_units = ['min', 'hours', 'days', 'weeks', 'month', 'year', 'decades']
        
        if duration_unit not in valid_units:
            await event.respond(f"Invalid duration unit. Choose from: {', '.join(valid_units)}")
            return
            
        success, result = await add_premium_user(target_user_id, duration_value, duration_unit)
        if success:
            expiry_utc = result
            expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
            formatted_expiry = expiry_ist.strftime('%d-%b-%Y %I:%M:%S %p')
            
            response = f"✅ User {target_user_id} added as premium member\nSubscription valid until: {formatted_expiry} (IST)"
            await event.respond(response)
            
            try:
                await bot_client.send_message(target_user_id, f"✅ You have been added as premium member\n**Validity upto**: {formatted_expiry} (IST)")
            except Exception:
                pass

            if PREMIUM_LOGS:
                try:
                    await bot_client.send_message(PREMIUM_LOGS, f"👤 **New Premium User**\n\n**User ID**: `{target_user_id}`\n**Duration**: {duration_value} {duration_unit}\n**Expiry**: {formatted_expiry} (IST)\n**Added by**: {user_id}")
                except Exception:
                    pass
        else:
            await event.respond(f'❌ Failed to add premium user: {result}')
    except ValueError:
        await event.respond('Invalid user ID or duration value. Both must be integers.')
    except Exception as e:
        await event.respond(f'Error: {str(e)}')


@bot_client.on(events.NewMessage(pattern='/revoke|/rem'))
async def revoke_premium_handler(event):
    if not await is_private_chat(event):
        return
        
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        return
        
    args = event.text.split()
    if len(args) != 2:
        await event.respond('Usage: /revoke user_id\nExample: /revoke 123456789')
        return
        
    try:
        target_user_id = int(args[1])
    except ValueError:
        await event.respond('❌ Invalid user ID.')
        return
        
    if not await is_premium_user(target_user_id):
        await event.respond(f'❌ User {target_user_id} does not have an active premium subscription.')
        return
        
    success = await revoke_premium_user(target_user_id)
    if success:
        await event.respond(f'✅ Premium subscription removed from {target_user_id}.')
        try:
            await bot_client.send_message(target_user_id, '⚠️ Your premium subscription has been removed by the administrator.')
        except Exception:
            pass
            
        if PREMIUM_LOGS:
            try:
                await bot_client.send_message(PREMIUM_LOGS, f"🚫 **Premium Removed**\n\n**User ID**: `{target_user_id}`\n**Removed by**: {user_id}")
            except Exception:
                pass
    else:
        await event.respond(f'❌ Failed to remove premium from user {target_user_id}.')


@bot_client.on(events.NewMessage(pattern='/extend'))
async def extend_premium_handler(event):
    if not await is_private_chat(event):
        return
    
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        return
        
    text = event.message.text.strip()
    parts = text.split(' ')
    if len(parts) != 4:
        await event.respond("Invalid format. Use: `/extend user_id duration_value duration_unit` \nExample: `/extend 123456 1 weeks`")
        return
        
    try:
        target_user_id = int(parts[1])
        duration_value = int(parts[2])
        duration_unit = parts[3].lower()
        valid_units = ['min', 'hours', 'days', 'weeks', 'month', 'year', 'decades']
        
        if duration_unit not in valid_units:
            await event.respond(f"Invalid duration unit. Choose from: {', '.join(valid_units)}")
            return
            
        success, result = await extend_premium_user(target_user_id, duration_value, duration_unit)
        if success:
            expiry_utc = result
            expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
            formatted_expiry = expiry_ist.strftime('%d-%b-%Y %I:%M:%S %p')
            
            response = f"✅ User {target_user_id} subscription extended\nNew expiry: {formatted_expiry} (IST)"
            await event.respond(response)
            
            try:
                await bot_client.send_message(target_user_id, f"✅ Your premium subscription has been extended\n**New validity**: {formatted_expiry} (IST)")
            except Exception:
                pass

            if PREMIUM_LOGS:
                try:
                    await bot_client.send_message(PREMIUM_LOGS, f"⏳ **Premium Extended**\n\n**User ID**: `{target_user_id}`\n**Added**: {duration_value} {duration_unit}\n**New Expiry**: {formatted_expiry} (IST)\n**Extended by**: {user_id}")
                except Exception:
                    pass
        else:
            await event.respond(f'❌ Failed to extend premium: {result}')
    except ValueError:
        await event.respond('Invalid user ID or duration value. Both must be integers.')
    except Exception as e:
        await event.respond(f'Error: {str(e)}')


@bot_client.on(events.NewMessage(pattern='/status'))
async def status_handler(event):
    if not await is_private_chat(event):
        return
    
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        return
    
    args = event.text.split()
    if len(args) != 2:
        await event.respond('Usage: /status user_id\nExample: /status 123456789')
        return
        
    try:
        target_user_id = int(args[1])
    except ValueError:
        await event.respond('❌ Invalid user ID.')
        return
        
    premium_details = await get_premium_details(target_user_id)
    
    if premium_details:
        expiry_utc = premium_details["subscription_end"]
        expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
        formatted_expiry = expiry_ist.strftime("%d-%b-%Y %I:%M:%S %p")
        
        await event.respond(
            f"**💎 Premium Status for `{target_user_id}`:**\n\n"
            f"**Status:** ✅ Active\n"
            f"**Expiry Date:** {formatted_expiry} (IST)\n"
        )
    else:
        await event.respond(f"**❌ User `{target_user_id}` does not have an active premium plan.**")


@bot_client.on(events.NewMessage(pattern='/myplan'))
async def myplan_handler(event):
    if not await is_private_chat(event):
        return
        
    user_id = event.sender_id
    premium_details = await get_premium_details(user_id)
    
    if premium_details:
        expiry_utc = premium_details["subscription_end"]
        expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
        formatted_expiry = expiry_ist.strftime("%d-%b-%Y %I:%M:%S %p")
        
        await event.respond(
            f"**💎 Your Premium Plan Details:**\n\n"
            f"**Status:** ✅ Active\n"
            f"**Expiry Date:** {formatted_expiry} (IST)\n\n"
            f"Thank you for being a premium member!"
        )
    else:
        await event.respond(
            "**❌ You don't have an active premium plan.**\n\n"
            "Use /plans to see available options."
        )


@bot_client.on(events.NewMessage(pattern='/plans'))
async def plans_handler(event):
    if not await is_private_chat(event):
        return
        
    plan_text = "**💎 Available Premium Plans:**\n\n"
    for plan_id, details in P0.items():
        plan_text += f"▪️ **{details['l']} Plan**\n"
        plan_text += f"  - Duration: {details['du']} {details['u']}\n"
        plan_text += f"  - Price: {details['s']} units\n\n"
    
    plan_text += f"Contact [Administrator]({AC}) to buy premium."
    
    await event.respond(plan_text, link_preview=False)


@bot_client.on(events.NewMessage(pattern='/paid'))
async def paid_handler(event):
    if not await is_private_chat(event):
        return
        
    paid_text = (
        "✨ **How to Pay?**\n\n"
        "You can purchase premium by contacting the admin directly or using the payment command if available.\n\n"
        f"**Admin**: @{OWNER_USERNAME}\n"
        f"**Contact Link**: {AC}\n\n"
        "After payment, please send the screenshot to the admin to get your premium activated."
    )
    
    await event.respond(paid_text, link_preview=False)


@bot_client.on(events.NewMessage(pattern='/getall'))
async def getall_handler(event):
    if not await is_private_chat(event):
        return
        
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        return
        
    premium_users = await get_all_premium_users()
    if not premium_users:
        await event.respond("No premium users found.")
        return
        
    response = "**👤 All Premium Users:**\n\n"
    for user in premium_users:
        u_id = user['user_id']
        expiry_utc = user['subscription_end']
        expiry_ist = expiry_utc + timedelta(hours=5, minutes=30)
        formatted_expiry = expiry_ist.strftime("%d-%b-%Y")
        response += f"• `{u_id}` - Exp: {formatted_expiry}\n"
        
        if len(response) > 3500:
            await event.respond(response)
            response = ""
            
    if response:
        await event.respond(response)


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    subscription_status = await subscribe(client, message)
    if subscription_status == 1:
        return

    start_text = (
        f"Hi 👋 Welcome to **{BRAND_NAME}**\n\n"
        "✅ I can save posts from channels or groups where forwarding is off. I can download videos/audio from YT, INSTA, and other social platforms.\n"
        "✅ Simply send the post link of a public channel. For private channels, use /login.\n"
        "✅ Send /help to know more about my features."
    )
    
    kb = IKM([
        [IK("Join Channel", url=JL)],
        [IK("Get Premium", url=AC)]
    ])

    await message.reply_photo(
        photo=START_PIC,
        caption=start_text,
        reply_markup=kb
    )
