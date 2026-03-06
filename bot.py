# AUTHOR: STARKIE
#OWNER OF CARELESS CODER

from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 31773201
API_HASH = "4de8b7e5dec61796c782bdc400759248"
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Client(
    "protection_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user_links = {}


# link detection
def has_link(text):
    if not text:
        return False
    links = ["http://", "https://", "t.me", "www."]
    text = text.lower()
    return any(link in text for link in links)


# LINK PROTECTION
@bot.on_message(filters.group & filters.text)
async def link_protection(client, message):

    if not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id

    member = await client.get_chat_member(chat_id, user_id)

    # ignore admins
    if member.status in ["administrator", "creator"]:
        return

    text = message.text

    if has_link(text):

        await message.delete()

        warn_text = f"""
🚫 Links are not allowed in this group.

Please do not send links.
"""

        await client.send_message(chat_id, warn_text)

        user_links[user_id] = user_links.get(user_id, 0) + 1

        # mute after 3 links
        if user_links[user_id] >= 3:

            await client.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions()
            )

            mute_text = f"""
🔇 {message.from_user.first_name} has been muted.

Reason: Sending too many links.
"""

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔓 Unmute",
                            callback_data=f"unmute_{user_id}"
                        )
                    ]
                ]
            )

            await client.send_message(
                chat_id,
                mute_text,
                reply_markup=buttons
            )

            user_links[user_id] = 0


# UNMUTE BUTTON
@bot.on_callback_query(filters.regex("^unmute_"))
async def unmute_user(client, callback_query):

    user_id = int(callback_query.data.split("_")[1])
    chat_id = callback_query.message.chat.id

    admin = await client.get_chat_member(chat_id, callback_query.from_user.id)

    # check if admin can restrict members
    if not (admin.status == "creator" or (admin.privileges and admin.privileges.can_restrict_members)):
        await callback_query.answer("❌ Only admins can unmute users.", show_alert=True)
        return

    await client.restrict_chat_member(
        chat_id,
        user_id,
        ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )

    await callback_query.message.edit_text(
        f"""✅ User has been unmuted by {callback_query.from_user.first_name}."""
    )


# EDITED MESSAGE DELETE
@bot.on_edited_message(filters.group)
async def delete_edited(client, message):

    if not message.from_user:
        return

    member = await client.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    if member.status in ["administrator", "creator"]:
        return

    try:
        await message.delete()
    except:
        pass


#-------------------------------------------#
# -----------------HELP---------------------#
#-------------------------------------------#

@bot.on_callback_query(filters.regex("help"))
async def help_menu(client, callback_query):

    text = f"""
<b>📖 BOT INSTRUCTIONS</b>

<b>• THIS BOT DELETES LINKS</b>
<b>• USERS SENDING TOO MANY LINKS GET MUTED</b>
<b>• EDITED MESSAGES ARE DELETED</b>
<b>• ADMINS ARE IGNORED</b>

<b>ADD THE BOT TO YOUR GROUP AND GIVE ADMIN PERMISSIONS.</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⬅️ Back", callback_data="back")]
        ]
    )

    await callback_query.message.edit_text(
        text,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML
    )

#-------------------------------------------#
# ------------START WELCOME ----------------#
#-------------------------------------------#

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):

    text = f"""
<b>HELLO {message.from_user.first_name} 👋</b>

<b>WELCOME TO THE PROTECTION BOT.</b>

<b>USE THE BUTTONS BELOW TO NAVIGATE.</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ ADD ME IN A GROUP", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true")],
            [
                InlineKeyboardButton("📖 HELP", callback_data="help"),
                InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")
            ]
        ]
    )

    await message.reply_photo(
        photo="YOUR_PHOTO_URL",
        caption=f"<tg-spoiler>{text}</tg-spoiler>",
        parse_mode=ParseMode.HTML,
        reply_markup=buttons
    )

#-------------------------------------------#
# -----------------ABOUT -------------------#
#-------------------------------------------#
@bot.on_callback_query(filters.regex("about"))
async def about_menu(client, callback_query):

    text = f"""
<b>ℹ️ ABOUT THIS BOT</b>

<b>OWNER:</b> @YOUR_USERNAME

<b>USE THE BUTTONS BELOW FOR SUPPORT OR UPDATES.</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👤 Owner", url="https://t.me/YOUR_USERNAME")
            ],
            [
                InlineKeyboardButton("📢 Support", url="https://t.me/YOUR_SUPPORT_LINK"),
                InlineKeyboardButton("📡 Updates", url="https://t.me/YOUR_UPDATE_LINK")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back")
            ]
        ]
    )

    await callback_query.message.edit_text(
        text,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML
    )

#----------------------#
#-----BACK BUTTON------#
#----------------------#

@bot.on_callback_query(filters.regex("back"))
async def back_menu(client, callback_query):

    text = f"""
<b>HELLO {callback_query.from_user.first_name} 👋</b>

<b>WELCOME TO THE PROTECTION BOT.</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ ADD ME IN A GROUP", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true")],
            [
                InlineKeyboardButton("📖 HELP", callback_data="help"),
                InlineKeyboardButton("ℹ️ ABOUT", callback_data="about")
            ]
        ]
    )

    await callback_query.message.reply_photo(
    photo="https://example.com/photo.jpg",
    caption=text,
    parse_mode=ParseMode.HTML,
    has_spoiler=True,
    reply_markup=buttons
    )

bot.run()
