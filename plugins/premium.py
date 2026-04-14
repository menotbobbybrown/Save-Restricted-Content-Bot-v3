# Copyright (c) 2025 Gagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import client as bot_client, app
from telethon import events
from datetime import datetime, timedelta
from config import OWNER_ID, PREMIUM_LOGS, P0, JOIN_LINK as JL , ADMIN_CONTACT as AC
from utils.func import add_premium_user, is_private_chat, get_premium_details, get_all_premium_users, premium_users_collection, is_premium_user, get_display_name
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton as IK, InlineKeyboardMarkup as IKM
import base64 as spy
from utils.func import a1, a2, a3, a4, a5, a7, a8, a9, a10, a11
from plugins.start import subscribe


@bot_client.on(events.NewMessage(pattern='/add'))
async def add_premium_handler(event):
    if not await is_private_chat(event):
        await event.respond('This command can only be used in private chats for security reasons.')
        return
    
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        await event.respond('This command is restricted to the bot owner.')
        return
        
    text = event.message.text.strip()
    parts = text.split(' ')
    if len(parts) != 4:
        await event.respond("Invalid format. Use: `/add user_id duration_value duration_unit` \nExample: `/add 123456 1 week`")
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
                await bot_client.send_message(target_user_id, f"✅ Your have been added as premium member\n**Validity upto**: {formatted_expiry} (IST)")
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


@bot_client.on(events.NewMessage(pattern='/rem'))
async def remove_premium_handler(event):
    if not await is_private_chat(event):
        await event.respond("This command can only be used in private chats.")
        return
        
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        await event.respond("This command is restricted to the bot owner.")
        return
        
    args = event.text.split()
    if len(args) != 2:
        await event.respond('Usage: /rem user_id\nExample: /rem 123456789')
        return
        
    try:
        target_user_id = int(args[1])
    except ValueError:
        await event.respond('❌ Invalid user ID.')
        return
        
    if not await is_premium_user(target_user_id):
        await event.respond(f'❌ User {target_user_id} does not have a premium subscription.')
        return
        
    try:
        result = await premium_users_collection.delete_one({'user_id': target_user_id})
        if result.deleted_count > 0:
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
    except Exception as e:
        await event.respond(f'❌ Error: {str(e)}')


@bot_client.on(events.NewMessage(pattern='/myplan'))
async def myplan_handler(event):
    if not await is_private_chat(event):
        await event.respond("This command can only be used in private chats.")
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
        await event.respond("This command can only be used in private chats.")
        return
        
    plan_text = "**💎 Available Premium Plans:**\n\n"
    for plan_id, details in P0.items():
        plan_text += f"▪️ **{details['l']} Plan**\n"
        plan_text += f"  - Duration: {details['du']} {details['u']}\n"
        plan_text += f"  - Price: {details['s']} units\n\n"
    
    plan_text += f"Contact [Administrator]({AC}) to buy premium."
    
    await event.respond(plan_text, link_preview=False)


@bot_client.on(events.NewMessage(pattern='/getall'))
async def getall_handler(event):
    if not await is_private_chat(event):
        await event.respond("This command can only be used in private chats.")
        return
        
    user_id = event.sender_id
    if user_id not in OWNER_ID:
        await event.respond("This command is restricted to the bot owner.")
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


attr1_enc = spy.b64encode("photo".encode()).decode()
attr2_enc = spy.b64encode("file_id".encode()).decode()

@app.on_message(filters.command(spy.b64decode(a5.encode()).decode()) & filters.private)
async def start_handler(client, message):
    subscription_status = await subscribe(client, message)
    if subscription_status == 1:
        return

    b1 = spy.b64decode(a1).decode()
    b2 = int(spy.b64decode(a2).decode())
    b3 = spy.b64decode(a3).decode()
    b4 = spy.b64decode(a4).decode()
    b6 = spy.b64decode(a7).decode()
    b7 = spy.b64decode(a8).decode()
    b8 = spy.b64decode(a9).decode()
    b9 = spy.b64decode(a10).decode()
    b10 = spy.b64decode(a11).decode()

    tm = await getattr(app, b3)(b1, b2)

    pb = getattr(tm, spy.b64decode(attr1_enc.encode()).decode())
    fd = getattr(pb, spy.b64decode(attr2_enc.encode()).decode())

    kb = IKM([
        [IK(b7, url=JL)],
        [IK(b8, url=AC)]
    ])

    await getattr(message, b4)(
        fd,
        caption=b6,
        reply_markup=kb
    )
