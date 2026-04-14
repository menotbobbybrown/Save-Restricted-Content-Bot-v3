# Copyright (c) 2025 Contributor : https://github.com/Contributor.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import app
from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOG_GROUP, OWNER_ID, FORCE_SUB, ADMIN_CONTACT, JOIN_LINK, BOT_NAME, START_PIC

async def subscribe(app, message):
    if FORCE_SUB:
        try:
          user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
          if str(user.status) == "ChatMemberStatus.BANNED":
              await message.reply_text(f"You are Banned. Contact -- {BOT_NAME} Support")
              return 1
        except UserNotParticipant:
            try:
                link = await app.export_chat_invite_link(FORCE_SUB)
            except:
                link = JOIN_LINK
            caption = f"Join our channel to use the bot"
            await message.reply_photo(photo=START_PIC, caption=caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now...", url=f"{link}")]]))
            return 1
        except Exception as e:
            await message.reply_text(f"Something Went Wrong. Contact admins... with following message {e}")
            return 1 
     
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        return
     
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("adl", "👻 Download audio"),
        BotCommand("dl", "💀 Download videos"),
        BotCommand("myplan", "🗓️ Check your premium plan"),
        BotCommand("plans", "📋 View available plans"),
        BotCommand("paid", "💰 Payment instructions"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("help", "❓ Help menu"),
        BotCommand("cancel", "🚫 Cancel process")
    ])
 
    await message.reply("✅ Commands configured successfully!")
 
 
help_pages = [
    (
        f"📝 **{BOT_NAME} Commands Overview (1/2)**:\n\n"
        "1. **/login**\n"
        "> Log into the bot for private channel access\n\n"
        "2. **/batch**\n"
        "> Bulk extraction for posts (After login)\n\n"
        "3. **/dl link**\n"
        "> Download videos from supported sites\n\n"
        "4. **/adl link**\n"
        "> Download audio from supported sites\n\n"
        "5. **/myplan**\n"
        "> Check your premium subscription details\n\n"
        "6. **/plans**\n"
        "> View available premium plans\n\n"
        "7. **/paid**\n"
        "> Payment instructions\n\n"
        "8. **/settings**\n"
        "> Personalize your bot experience\n\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "9. **/logout**\n"
        "> Logout from the bot\n\n"
        "10. **/stats**\n"
        "> Get bot stats\n\n"
        "11. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "12. **/settings** details:\n"
        "> - SETCHATID : To directly upload in channel or group\n"
        "> - SETRENAME : To add custom rename tag\n"
        "> - CAPTION : To add custom caption\n"
        "> - REPLACEWORDS : Replace specific words in captions\n"
        "> - RESET : Reset settings to default\n\n"
        f"**__Powered by {BOT_NAME}__**"
    )
]
 
 
async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return
 
    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")
 
    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)
 
    keyboard = InlineKeyboardMarkup([buttons])
 
    try:
        await message.delete()
    except:
        pass
 
    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )
 
 
@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return
     
    await send_or_edit_help_page(client, message, 0)
 
 
@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])
 
    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    await send_or_edit_help_page(client, callback_query.message, page_number)
    await callback_query.answer()


@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url=ADMIN_CONTACT)],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)
 
 
@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "> 💰 **Premium Price**:\n\n"
        "Check /plans for more information on available pricing and options.\n"
        "📥 **Download Limit**: Higher limits for premium users.\n"
        "🛑 **Batch**: Access to bulk extraction tools.\n\n"
        "📜 **Terms and Conditions**: For further details, please send /terms.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url=ADMIN_CONTACT)],
        ]
    )
    await message.reply_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "> 💰 **Premium Price**:\n\n"
        "Check /plans for more information on available pricing and options.\n"
        "📥 **Download Limit**: Higher limits for premium users.\n"
        "🛑 **Batch**: Access to bulk extraction tools.\n\n"
        "📜 **Terms and Conditions**: For further details, please send /terms.\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Now", url=ADMIN_CONTACT)],
        ]
    )
    await callback_query.message.edit_text(plan_text, reply_markup=buttons)
 
 
@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
    )
     
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Now", url=ADMIN_CONTACT)],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)
