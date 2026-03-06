# AUTHOR: STARKIE
#OWNER OF CARELESS CODER

from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
import re   # <-- regex ke liye zaroori

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


#link system --------
def has_link(text):
    if not text:
        return False
    text = text.lower()
    # general links
    link_pattern = r"(https?://|www\.|t\.me/|telegram\.me/)"
    # channel/group usernames
    channel_pattern = r"@(\w*(group|channel|bot)\w*)"
    if re.search(link_pattern, text):
        return True
    if re.search(channel_pattern, text):
        return True
    return False


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

        warn_text = f"""⚠️ 𝐖𝐀𝐑𝐍𝐈𝐍𝐆 : 
<b>🚫 ʟɪηᴋꜱ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪη ᴛʜɪꜱ ɢʀᴏᴜᴘ.</b>
<b>❌ ᴘʟᴇᴀꜱᴇ ᴅᴏ ɴᴏᴛ sᴇηᴅ ʟɪηᴋꜱ.</b>
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

    text = f"""<b>╔══❖ 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 𝐏𝐀𝐍𝐄𝐋𝐋 ❖══╗</b

<b>❍</b> 𝐈𝐌𝐏𝐎𝐑𝐓𝐀𝐍𝐓 𝐏𝐄𝐑𝐌𝐈𝐒𝐒𝐈𝐎𝐍:<br>
<blockquote>
<b>➻ ᴄʜᴀηɢᴇ ɢʀᴏᴜᴘ ɪηꜰᴏ</b><br>
<b>➻ ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ</b><br>
<b>➻ ʀɪꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ</b><br>
<b>➻ ʙᴀη / ᴍᴜᴛᴇ ᴜꜱᴇʀꜱ</b>
</blockquote>

<b>❍</b> 𝐖𝐇𝐀𝐓 𝐖𝐈𝐋𝐋 𝐓𝐇𝐄 𝐁𝐎𝐓 𝐃𝐎 ?<br>
<blockquote>
<b>➻ ʟʟ ʟɪηᴋꜱ ʙʟᴏᴄᴋᴇᴅ</b><br>
<b>➻ ᴇᴅɪᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ᴧᴜᴛᴏ ᴅᴇʟᴇᴛᴇᴅ</b><br>
<b>➻ ɪꜰ ᴀηʏ ᴍᴇᴍʙᴇʀ sᴇηᴅꜱ ᴀ ʟɪηᴋ, ʙᴏᴛ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ɪᴛ ᴧηᴅ ɢɪᴠᴇ ᴀ ᴡᴀʀɴɪηɢ</b><br>
<b>➻ ᴀꜰᴛᴇʀ 3 ᴡᴀʀɴɪηɢꜱ, ᴜꜱᴇʀ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴍᴜᴛᴇᴅ</b><br>
<b>➻ ᴏηʟʏ ᴀᴅᴍɪηꜱ/ᴏᴡɴᴇʀꜱ ᴄᴀη ʀᴇᴍᴏᴠᴇ ᴍᴜᴛᴇ ʀᴇꜱᴛʀɪᴄᴛɪᴏη</b><br>
<b>➻ ɴᴏ ʀᴇꜱᴛʀɪᴄᴛɪᴏηꜱ ᴏη ᴇᴅɪᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ</b>
</blockquote>

➤ <b>ɪꜰ ʏᴏᴜ ᴡᴀηᴛ ᴛᴏ ᴄᴏηᴛᴀᴄᴛ ᴜꜱ, ᴘʟᴇᴀꜱᴇ ᴠɪꜱɪᴛ ᴛʜᴇ ᴀʙᴏᴜᴛ ꜱᴇᴄᴛɪᴏη.</b>

"""

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⌯ 🔙 ʙᴀᴄᴋ ⌯", callback_data="back")]
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

    text = f"""<b>👋 ʜᴇʟʟᴏ {message.from_user.first_name} 💕</b>
<b>❍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ˹𝐏ʀᴏᴛᴇᴄᴛɪᴏɴ˼  . 🥳</b>
✦━━━━━━━━━━━━━━━━━━━━✦
<b>🛠  ɪ ᴘʀᴏᴛᴇᴄᴛ ɢʀᴏᴜᴘꜱ ꜰʀᴏᴍ:</b>
<b>➜ ᴇxᴛᴇʀηᴧʟ ʟɪηᴋꜱ 🚫</b>
<b>➜ ᴇᴅɪᴛᴇᴅ ᴍᴇꜱꜱᴧɢᴇꜱ ✏️</b>
<b>➜ ʟɪɴᴋs sᴘᴀᴍᴍɪɴɢ 🔗</b>
<b>➜ Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ℹ️ </b>
<b>✦━━━━━━━━━━━━━━━━━━━━━✦</b>
<b>➤ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href="https://t.me/CarelessxOwner">˹ᴍɪsᴛᴇʀ ꭙ sᴛᴀʀᴋ˼</a></b>
<b>➤ ᴍᴏʀᴇ ʙᴏᴛs : <a href="https://t.me/StarkxNetwrk">˹sᴛᴀʀᴋ ꭙ ɴᴇᴛᴡᴏʀᴋ˼</a></b>
<b>➤ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : <a href="https://t.me/ll_CarelessxCoder_ll">˹ᴄᴀʀᴇʟᴇss ꭙ ᴄᴏᴅᴇʀ˼</a></b>
<b>╰─━━━  ✦ ❀ ✦ ❖ ✦ ❀ ✦   ━━━─</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⌯ ➕ ᴀᴅᴅ ᴍᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ ⌯", url="https://t.me/Protectioncc_bot?startgroup=true")],
            [
                InlineKeyboardButton("⌯ ℹ️ ʜᴇʟᴘ ⌯", callback_data="help"),
                InlineKeyboardButton("⌯ 🧑🏻‍💻 ᴀʙᴏᴜᴛ ⌯", callback_data="about")
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

    text = f"""<b>╭─━━━ ✦ ᴀʙᴏᴜᴛ ʙᴏᴛ ✦ ━━━─╮</b>
<b>│</b>
<b>│ 🤖 ɴᴀᴍᴇ : ᴍɪsᴛᴇʀ sᴛᴀʀᴋ</b>
<b>│ 👑 ᴏᴡɴᴇʀ : <a href="https://t.me/CarelessxOwner">˹ᴍɪsᴛᴇʀ ꭙ sᴛᴀʀᴋ˼</a></b>
<b>│ 📢 ᴜᴘᴅᴀᴛᴇs : <a href="https://t.me/ll_CarelessxCoder_ll">˹ᴄᴀʀᴇʟᴇss ꭙ ᴄᴏᴅᴇʀ˼</a></b>
<b>│ 🚀 ᴠᴇʀsɪᴏɴ : v2.6</b>
<b>│ 🐍 ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ 3</b>
<b>│ 📚 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ</b>
<b>│ 📡 ʜᴏsᴛᴇᴅ ᴏɴ : ᴠᴘs</b>
<b>│</b>
<b>╰━ ✦ ᴘᴏᴡᴇʀᴇᴅ ʙʏ <a href="https://t.me/ll_CarelessxCoder_ll">˹ᴄᴀʀᴇʟᴇss ꭙ ᴄᴏᴅᴇʀ˼</a></b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⌯ ❍ᴡηєʀ ⌯", url="https://t.me/YOUR_USERNAME")
            ],
            [
                InlineKeyboardButton("⌯ sᴜᴘᴘσʀᴛ ⌯", url="https://t.me/CarelessxWorld"),
                InlineKeyboardButton("⌯ ᴜᴘᴅᴀᴛᴇ ⌯", url="https://t.me/ll_CarelessxCoder_ll")
            ],
            [
                InlineKeyboardButton("⌯ 🔙 ʙᴀᴄᴋ ⌯", callback_data="back")
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

    text = f"""<b>👋 ʜᴇʟʟᴏ {message.from_user.first_name} 💕</b>
<b>❍ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ˹𝐏ʀᴏᴛᴇᴄᴛɪᴏɴ˼  . 🥳</b>
✦━━━━━━━━━━━━━━━━━━━━━✦
<b>🛠  ɪ ᴘʀᴏᴛᴇᴄᴛ ɢʀᴏᴜᴘꜱ ꜰʀᴏᴍ:</b>
<b>➜ ᴇxᴛᴇʀηᴧʟ ʟɪηᴋꜱ 🚫</b>
<b>➜ ᴇᴅɪᴛᴇᴅ ᴍᴇꜱꜱᴧɢᴇꜱ ✏️</b>
<b>➜ ʟɪɴᴋs sᴘᴀᴍᴍɪɴɢ 🔗</b>
<b>➜ Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ℹ️ </b>
<b>✦━━━━━━━━━━━━━━━━━━━━━✦</b>
<b>➤ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href="https://t.me/CarelessxOwner">˹ᴍɪsᴛᴇʀ ꭙ sᴛᴀʀᴋ˼</a></b>
<b>➤ ᴍᴏʀᴇ ʙᴏᴛs : <a href="https://t.me/StarkxNetwrk">˹sᴛᴀʀᴋ ꭙ ɴᴇᴛᴡᴏʀᴋ˼</a></b>
<b>➤ ᴘᴏᴡᴇʀᴇᴅ ʙʏ : <a href="https://t.me/ll_CarelessxCoder_ll">˹ᴄᴀʀᴇʟᴇss ꭙ ᴄᴏᴅᴇʀ˼</a></b>
<b>╰─━━━  ✦ ❀ ✦ ❖ ✦ ❀ ✦   ━━━─</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⌯ ➕ ᴀᴅᴅ ᴍᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ ⌯", url="https://t.me/Protectioncc_bot?startgroup=true")],
            [
                InlineKeyboardButton("⌯ ℹ️ ʜᴇʟᴘ ⌯", callback_data="help"),
                InlineKeyboardButton("⌯ 🧑🏻‍💻 ᴀʙᴏᴜᴛ ⌯", callback_data="about")
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
