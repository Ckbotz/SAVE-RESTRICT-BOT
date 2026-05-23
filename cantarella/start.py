# Developed by: LastPerson07 × cantarella
# Telegram: @cantarellabots | @THEUPDATEDGUYS
import os
import asyncio
import random
import time
import shutil
import pyrogram
import requests
import hashlib
from pyrogram import Client, filters, enums
from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant,
    InviteHashExpired, UsernameNotOccupied, AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto
from config import API_ID, API_HASH, ERROR_MESSAGE
from database.db import db
import math
from logger import LOGGER

# --- Import additional features from additional.py ---
from cantarella.additional import (
    clean_filename,
    apply_prefix_suffix,
    smart_sleep,
    download_thumbnail,
    add_metadata_with_ffmpeg,
    PERMANENT_THUMBNAIL_URL,
    CUSTOM_SLEEP,
)

logger = LOGGER(__name__)
SUBSCRIPTION = os.environ.get('SUBSCRIPTION', 'https://graph.org/file/242b7f1b52743938d81f1.jpg')
FREE_LIMIT_SIZE = 2 * 1024 * 1024 * 1024
FREE_LIMIT_DAILY = 10
UPI_ID = os.environ.get("UPI_ID", "your_upi@oksbi")
QR_CODE = os.environ.get("QR_CODE", "https://graph.org/file/242b7f1b52743938d81f1.jpg")
REACTIONS = [
    "👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬",
    "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱",
    "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌",
    "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴",
    "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝",
    "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒",
    "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", "🤷‍♀️",
    "😡"
]

dev_text = "👨‍💻 Mind Behind This Bot:\n• @DmOwner\n• @akaza7902"
expected_dev_hash = "b9e63b7578bdec13f3cb3162fe5f5e93dccaba3bfd5c8ddacbb90ffdcdcce402"
channels_text = "📢 Official Channels:\n• @ReX_update\n• @THEUPDATEDGUYS\n\nStay updated for new features!"
expected_channels_hash = "e19212e571bd0f6626450dd790029d392c0748c554d4b386a0c0752f4148d37d"

if (
    hashlib.sha256(dev_text.encode('utf-8')).hexdigest() != expected_dev_hash or
    hashlib.sha256(channels_text.encode('utf-8')).hexdigest() != expected_channels_hash
):
    raise Exception("Tampered developer info detected! Bot will not start. Fuck the code - crashing now.")


class script(object):

    START_TXT = """<b>👋 Hello {},</b>
<b>🤖 I am <a href=https://t.me/{}>{}</a></b>
<i>Your Professional Restricted Content Saver Bot.</i>
<blockquote><b>🚀 System Status: 🟢 Online</b>
<b>⚡ Performance: 10x High-Speed Processing</b>
<b>🔐 Security: End-to-End Encrypted</b>
<b>📊 Uptime: 99.9% Guaranteed</b></blockquote>
<b>👇 Select an Option Below to Get Started:</b>
"""
    HELP_TXT = """<b>📚 Comprehensive Help & User Guide</b>
<blockquote><b>1️⃣ Public Channels (No Login Required)</b></blockquote>
• Forward or send the post link directly.
• Compatible with any public channel or group.
• <i>Example Link:</i> <code>https://t.me/channel/123</code>
<blockquote><b>2️⃣ Private/Restricted Channels (Login Required)</b></blockquote>
• Use <code>/login</code> to securely connect your Telegram account.
• Send the private link (e.g., <code>t.me/c/123...</code>).
• Bot accesses content using your authenticated session.
<blockquote><b>3️⃣ Batch Downloading Mode</b></blockquote>
• Initiate with <code>/batch</code> for multiple files.
• Follow interactive prompts for seamless processing.
<blockquote><b>🛑 Free User Limitations:</b></blockquote>
• <b>Daily Quota:</b> 10 Files / 24 Hours
• <b>File Size Cap:</b> 2GB Maximum
<blockquote><b>💎 Premium Membership Benefits:</b></blockquote>
• Unlimited Downloads & No Restrictions.
• Priority Support & Advanced Features.
<blockquote><b>🕐 Batch Sleep Settings:</b></blockquote>
• Use <code>/setsleep 3 5 7 10</code> to set custom delay between downloads.
• Use <code>/getsleep</code> to view your current sleep settings.
"""
    ABOUT_TXT = """<b>ℹ️ About This Bot</b>
<blockquote><b>╭────[ 🧩 Technical Stack ]────⍟</b>
<b>├⍟ 🤖 Bot Name : <a href=http://t.me/THEUPDATEDGUYS_Bot>Save Content</a></b>
<b>├⍟ 👨‍💻 Developer : <a href=https://t.me/DmOwner>Ⓜ️ark X cantarella</a></b>
<b>├⍟ 📚 Library : <a href='https://docs.pyrogram.org/'>Pyrogram Async</a></b>
<b>├⍟ 🐍 Language : <a href='https://www.python.org/'>Python 3.11+</a></b>
<b>├⍟ 🗄 Database : <a href='https://www.mongodb.com/'>MongoDB Atlas Cluster</a></b>
<b>├⍟ 📡 Hosting : Dedicated High-Speed VPS</b>
<b>╰───────────────⍟</b></blockquote>
"""
    PREMIUM_TEXT = """<b>💎 Premium Membership Plans</b>
<b>Unlock Unlimited Access & Advanced Features!</b>
<blockquote><b>✨ Key Benefits:</b>
<b>♾️ Unlimited Daily Downloads</b>
<b>📂 Support for 4GB+ File Sizes</b>
<b>⚡ Instant Processing (Zero Delay)</b>
<b>🖼 Customizable Thumbnails</b>
<b>📝 Personalized Captions</b>
<b>🛂 24/7 Priority Support</b></blockquote>
<blockquote><b>💳 Pricing Options:</b></blockquote>
• <b>1 Month Plan:</b> ₹50 / $1 (Billed Monthly)
• <b>3 Month Plan:</b> ₹120 / $2.5 (Save 20%)
• <b>Lifetime Access:</b> ₹200 / $4 (One-Time Payment)
<blockquote><b>👇 Secure Payment:</b></blockquote>
<b>💸 UPI ID:</b> <code>{}</code>
<b>📸 QR Code:</b> <a href='{}'>Scan to Pay</a>
<i>After Payment: Send Screenshot to Admin for Instant Activation.</i>
"""
    PROGRESS_BAR = """\
<b>⚡ Processing Task...</b>
<blockquote>
<b>Progress: {bar} {percentage:.1f}%</b>
<b>🚀 Speed:</b> <code>{speed}/s</code>
<b>💾 Size:</b> <code>{current} of {total}</code>
<b>⏱ Elapsed:</b> <code>{elapsed}</code>
<b>⏳ ETA:</b> <code>{eta}</code>
</blockquote>
"""
    CAPTION = """<b><a href="https://t.me/THEUPDATEDGUYS"></a></b>\n\n<b>⚜️ Powered By : <a href="https://t.me/THEUPDATEDGUYS">THE UPDATED GUYS 😎</a></b>"""
    LIMIT_REACHED = """<b>🚫 Daily Limit Exceeded</b>
<b>Your 10 free saves for today have been used.</b>
<i>Quota resets automatically after 24 hours from first download.</i>
<blockquote><b>🔓 Upgrade to Premium for Unlimited Access!</b></blockquote>
Remove all restrictions and enjoy seamless downloading.
"""
    SIZE_LIMIT = """<b>⚠️ File Size Exceeded</b>
<b>Free tier limited to 2GB per file.</b>
<blockquote><b>🔓 Upgrade to Premium</b></blockquote>
Download files up to 4GB and beyond with no limits!
"""


def humanbytes(size):
    if not size:
        return "0B"
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2] if tmp else "0s"


class batch_temp(object):
    IS_BATCH = {}


def get_message_type(msg):
    if getattr(msg, 'document', None): return "Document"
    if getattr(msg, 'video', None): return "Video"
    if getattr(msg, 'photo', None): return "Photo"
    if getattr(msg, 'audio', None): return "Audio"
    if getattr(msg, 'text', None): return "Text"
    return None


# =====================================================================
# Core download logic — UNTOUCHED from Code 1
# =====================================================================

async def downstatus(client, statusfile, message, chat):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        try:
            with open(statusfile, "r", encoding='utf-8') as downread:
                txt = downread.read()
            await client.edit_message_text(chat, message.id, f"{txt}")
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)


async def upstatus(client, statusfile, message, chat):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        try:
            with open(statusfile, "r", encoding='utf-8') as upread:
                txt = upread.read()
            await client.edit_message_text(chat, message.id, f"{txt}")
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)


def progress(current, total, message, type):
    if batch_temp.IS_BATCH.get(message.from_user.id):
        raise Exception("Cancelled")
    if not hasattr(progress, "cache"):
        progress.cache = {}

    now = time.time()
    task_id = f"{message.id}{type}"
    last_time = progress.cache.get(task_id, 0)

    if not hasattr(progress, "start_time"):
        progress.start_time = {}
    if task_id not in progress.start_time:
        progress.start_time[task_id] = now

    if (now - last_time) > 5 or current == total:
        try:
            percentage = current * 100 / total
            speed = current / (now - progress.start_time[task_id]) if (now - progress.start_time[task_id]) > 0 else 0
            eta = (total - current) / speed if speed > 0 else 0
            elapsed = now - progress.start_time[task_id]

            filled_length = int(percentage / 5)
            bar = '█' * filled_length + ' ' * (20 - filled_length)

            status = script.PROGRESS_BAR.format(
                bar=bar,
                percentage=percentage,
                current=humanbytes(current),
                total=humanbytes(total),
                speed=humanbytes(speed),
                elapsed=TimeFormatter(elapsed * 1000),
                eta=TimeFormatter(eta * 1000)
            )

            with open(f'{message.id}{type}status.txt', "w", encoding='utf-8') as fileup:
                fileup.write(status)

            progress.cache[task_id] = now

            if current == total:
                progress.start_time.pop(task_id, None)
                progress.cache.pop(task_id, None)
        except:
            pass


# =====================================================================
# Command handlers
# =====================================================================

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
    apis = ["https://api.waifu.pics/sfw/waifu", "https://nekos.life/api/v2/img/waifu"]
    api_url = random.choice(apis)
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        photo_url = response.json()["url"]
    except Exception as e:
        logger.error(f"Failed to fetch image from API: {e}")
        photo_url = "https://i.postimg.cc/kX9tjGXP/16.png"
    buttons = [
        [
            InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
            InlineKeyboardButton("🆘 Help & Guide", callback_data="help_btn")
        ],
        [
            InlineKeyboardButton("⚙️ Settings Panel", callback_data="settings_btn"),
            InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
        ],
        [
            InlineKeyboardButton('📢 Channels', callback_data="channels_info"),
            InlineKeyboardButton('👨‍💻 Developers', callback_data="dev_info")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    bot = await client.get_me()
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=script.START_TXT.format(message.from_user.mention, bot.username, bot.first_name),
        reply_markup=reply_markup,
        reply_to_message_id=message.id,
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    buttons = [[InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]]
    await client.send_message(
        chat_id=message.chat.id,
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.command(["plan", "myplan", "premium"]))
async def send_plan(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("📸 Send Payment Proof", url="https://t.me/DmOwner")],
        [InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]
    ]
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SUBSCRIPTION,
        caption=script.PREMIUM_TEXT.format(UPI_ID, QR_CODE),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await message.reply_text("❌ Batch Process Cancelled Successfully.")


# =====================================================================
# Additional feature commands — /setsleep and /getsleep
# =====================================================================

@Client.on_message(filters.command(["setsleep"]) & filters.private)
async def set_sleep(client: Client, message: Message):
    try:
        parts = message.text.split()[1:]
        if not parts:
            await message.reply(
                "**Usage:** `/setsleep 3 5 7 10`\n\n"
                "Provide space-separated sleep values in seconds.\n"
                "Bot will randomly pick one value for each download to avoid detection.\n\n"
                "**Allowed range:** 1-1000 seconds\n"
                "**Example:** `/setsleep 3 5 7 10 12 15`"
            )
            return

        sleep_values = [int(x) for x in parts if x.isdigit() and 1 <= int(x) <= 1000]

        if not sleep_values:
            await message.reply("❌ Please provide valid sleep values between 1-1000 seconds!")
            return

        CUSTOM_SLEEP[message.from_user.id] = sleep_values
        await message.reply(
            f"✅ **Sleep values set successfully!**\n\n"
            f"Values: `{', '.join(map(str, sleep_values))}` seconds\n"
            f"Bot will randomly pick one value between downloads.\n\n"
            f"💡 **Tip:** More varied values = better anti-detection!"
        )
    except ValueError:
        await message.reply("❌ Please provide valid numeric values only!")


@Client.on_message(filters.command(["getsleep"]) & filters.private)
async def get_sleep(client: Client, message: Message):
    sleep_values = CUSTOM_SLEEP.get(message.from_user.id, [3, 5, 7, 10])
    await message.reply(
        f"**⏱️ Current Sleep Settings:**\n\n"
        f"Values: `{', '.join(map(str, sleep_values))}` seconds\n"
        f"Random selection with ±20% jitter for natural behavior.\n\n"
        f"Use `/setsleep` to change these values."
    )


async def settings_panel(client, callback_query):
    """Renders the Settings Menu with professional layout."""
    user_id = callback_query.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = "💎 Premium Member" if is_premium else "👤 Standard User"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Command List", callback_data="cmd_list_btn")],
        [InlineKeyboardButton("📊 Usage Stats", callback_data="user_stats_btn")],
        [InlineKeyboardButton("🗑 Dump Chat Settings", callback_data="dump_chat_btn")],
        [InlineKeyboardButton("🖼 Manage Thumbnail", callback_data="thumb_btn")],
        [InlineKeyboardButton("📝 Edit Caption", callback_data="caption_btn")],
        [InlineKeyboardButton("⬅️ Return to Home", callback_data="start_btn")]
    ])

    text = (
        f"<b>⚙️ Settings Dashboard</b>\n\n"
        f"<b>Account Status:</b> {badge}\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n\n"
        f"<i>Customize and manage your bot preferences below for an optimized experience:</i>"
    )

    await callback_query.edit_message_caption(
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )


# =====================================================================
# Main save handler — core logic UNTOUCHED
# sleep between batch items replaced with smart_sleep from additional.py
# =====================================================================

@Client.on_message(filters.text & filters.private & ~filters.regex("^/"))
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:

        is_limit_reached = await db.check_limit(message.from_user.id)
        if is_limit_reached:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=script.LIMIT_REACHED,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )

        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            return await message.reply_text(
                "<b>⚠️ A Task is Currently Processing.</b>\n"
                "<i>Please wait for completion or use /cancel to stop.</i>",
                parse_mode=enums.ParseMode.HTML
            )

        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        batch_temp.IS_BATCH[message.from_user.id] = False
        is_private_link = "https://t.me/c/" in message.text
        is_batch = "https://t.me/b/" in message.text
        is_public_link = not is_private_link and not is_batch

        for msgid in range(fromID, toID + 1):

            if batch_temp.IS_BATCH.get(message.from_user.id):
                break

            if is_public_link:
                username = datas[3]
                try:
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=username,
                        message_id=msgid,
                        reply_to_message_id=message.id
                    )
                    await db.add_traffic(message.from_user.id)
                    # smart_sleep instead of fixed asyncio.sleep(1)
                    await smart_sleep(message.from_user.id)
                    continue
                except Exception as e:
                    pass

            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply(
                    "<b>🔒 Authentication Required</b>\n\n"
                    "<i>Access to this content requires login.</i>\n"
                    "<i>Use /login to securely authorize your account.</i>",
                    parse_mode=enums.ParseMode.HTML
                )
                batch_temp.IS_BATCH[message.from_user.id] = True
                return

            try:
                acc = Client(
                    "saverestricted",
                    session_string=user_data,
                    api_hash=API_HASH,
                    api_id=API_ID,
                    in_memory=True,
                    max_concurrent_transmissions=10
                )
                await acc.connect()
            except Exception as e:
                batch_temp.IS_BATCH[message.from_user.id] = True
                return await message.reply(
                    f"<b>❌ Authentication Failed</b>\n\n"
                    f"<i>Your session may have expired. Please /logout and /login again.</i>\n"
                    f"<code>{e}</code>",
                    parse_mode=enums.ParseMode.HTML
                )

            if is_private_link:
                chatid = int("-100" + datas[4])
                await handle_restricted_content(client, acc, message, chatid, msgid)
            elif is_batch:
                username = datas[4]
                await handle_restricted_content(client, acc, message, username, msgid)
            else:
                username = datas[3]
                await handle_restricted_content(client, acc, message, username, msgid)

            # smart_sleep instead of fixed asyncio.sleep(2)
            await smart_sleep(message.from_user.id)

        batch_temp.IS_BATCH[message.from_user.id] = True


# =====================================================================
# handle_restricted_content — core download/upload logic UNTOUCHED
# Additional features (clean_filename, prefix/suffix, metadata,
# permanent thumbnail) applied AFTER download, BEFORE upload
# =====================================================================

async def handle_restricted_content(client: Client, acc, message: Message, chat_target, msgid):
    try:
        msg: Message = await acc.get_messages(chat_target, msgid)
    except Exception as e:
        logger.error(f"Error fetching message: {e}")
        return
    if msg.empty:
        return

    msg_type = get_message_type(msg)
    if not msg_type:
        return

    file_size = 0
    if msg_type == "Document": file_size = msg.document.file_size
    elif msg_type == "Video": file_size = msg.video.file_size
    elif msg_type == "Audio": file_size = msg.audio.file_size

    if file_size > FREE_LIMIT_SIZE:
        if not await db.check_premium(message.from_user.id):
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            await client.send_message(
                message.chat.id,
                script.SIZE_LIMIT,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
            return

    if msg_type == "Text":
        try:
            await client.send_message(message.chat.id, msg.text, entities=msg.entities, parse_mode=enums.ParseMode.HTML)
            return
        except:
            return

    await db.add_traffic(message.from_user.id)
    smsg = await client.send_message(
        message.chat.id,
        '<b>⬇️ Starting Download...</b>',
        reply_to_message_id=message.id,
        parse_mode=enums.ParseMode.HTML
    )

    temp_dir = f"downloads/{message.id}"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # --- DOWNLOAD (core logic untouched) ---
    try:
        asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, message.chat.id))

        file = await acc.download_media(
            msg,
            file_name=f"{temp_dir}/",
            progress=progress,
            progress_args=[message, "down"]
        )

        if os.path.exists(f'{message.id}downstatus.txt'):
            os.remove(f'{message.id}downstatus.txt')

    except Exception as e:
        if batch_temp.IS_BATCH.get(message.from_user.id) or "Cancelled" in str(e):
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return await smsg.edit("❌ **Task Cancelled**")
        return await smsg.delete()

    # --- POST-DOWNLOAD: apply additional features before upload ---
    if file and os.path.exists(file):
        old_filename = os.path.basename(file)
        dir_name = os.path.dirname(file)

        # 1. Clean filename (remove unwanted words)
        cleaned = clean_filename(old_filename)
        # 2. Apply prefix / suffix
        final_filename = apply_prefix_suffix(cleaned)

        if old_filename != final_filename:
            new_path = os.path.join(dir_name, final_filename)
            os.rename(file, new_path)
            file = new_path

        # 3. Add metadata via ffmpeg (no-op if env vars not set)
        file, _ = await add_metadata_with_ffmpeg(file, final_filename)

    # --- UPLOAD (core logic untouched) ---
    try:
        asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, message.chat.id))

        ph_path = None

        # 4. Permanent thumbnail (from additional.py) — overrides DB thumb if set
        if PERMANENT_THUMBNAIL_URL:
            ph_path = await download_thumbnail(PERMANENT_THUMBNAIL_URL)

        # Fall back to DB custom thumbnail if no permanent one
        if not ph_path:
            thumb_id = await db.get_thumbnail(message.from_user.id)
            if thumb_id:
                try:
                    ph_path = await client.download_media(thumb_id, file_name=f"{temp_dir}/custom_thumb.jpg")
                except Exception as e:
                    logger.error(f"Failed to download custom thumb: {e}")

        # Fall back to original video/document thumbnail
        if not ph_path:
            try:
                if msg_type == "Video" and msg.video.thumbs:
                    ph_path = await acc.download_media(msg.video.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
                elif msg_type == "Document" and msg.document.thumbs:
                    ph_path = await acc.download_media(msg.document.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
            except:
                pass

        custom_caption = await db.get_caption(message.from_user.id)
        if custom_caption:
            final_caption = custom_caption.format(filename=file.split("/")[-1], size=humanbytes(file_size))
        else:
            final_caption = script.CAPTION.format(file_name=file.split("/")[-1])
            if msg.caption:
                final_caption += f"\n\n{msg.caption}"

        if msg_type == "Document":
            await client.send_document(
                message.chat.id, file, thumb=ph_path, caption=final_caption,
                progress=progress, progress_args=[message, "up"]
            )
        elif msg_type == "Video":
            await client.send_video(
                message.chat.id, file,
                duration=msg.video.duration, width=msg.video.width, height=msg.video.height,
                thumb=ph_path, caption=final_caption,
                progress=progress, progress_args=[message, "up"]
            )
        elif msg_type == "Audio":
            await client.send_audio(
                message.chat.id, file, thumb=ph_path, caption=final_caption,
                progress=progress, progress_args=[message, "up"]
            )
        elif msg_type == "Photo":
            await client.send_photo(message.chat.id, file, caption=final_caption)

    except Exception as e:
        await smsg.edit(f"Upload Failed: {e}")

    # Cleanup permanent thumbnail temp file
    if ph_path and PERMANENT_THUMBNAIL_URL and os.path.exists(ph_path):
        try:
            os.remove(ph_path)
        except:
            pass

    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    await client.delete_messages(message.chat.id, [smsg.id])


# =====================================================================
# Callback query handler — untouched from Code 1
# =====================================================================

@Client.on_callback_query()
async def button_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message
    if not message:
        return

    if data == "dev_info":
        await callback_query.answer(text=dev_text, show_alert=True)

    elif data == "channels_info":
        await callback_query.answer(text=channels_text, show_alert=True)

    elif data == "settings_btn":
        await settings_panel(client, callback_query)

    elif data == "buy_premium":
        buttons = [
            [InlineKeyboardButton("📸 Send Payment Proof", url="https://t.me/DmOwner")],
            [InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]
        ]
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=SUBSCRIPTION,
                caption=script.PREMIUM_TEXT.format(callback_query.from_user.mention, UPI_ID, QR_CODE)
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "help_btn":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "about_btn":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "start_btn":
        bot = await client.get_me()
        apis = ["https://api.waifu.pics/sfw/waifu", "https://nekos.life/api/v2/img/waifu"]
        api_url = random.choice(apis)
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            photo_url = response.json()["url"]
        except Exception as e:
            logger.error(f"Failed to fetch image from API: {e}")
            photo_url = "https://i.postimg.cc/cC7txyhz/15.png"
        buttons = [
            [
                InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
                InlineKeyboardButton("🆘 Help & Guide", callback_data="help_btn")
            ],
            [
                InlineKeyboardButton("⚙️ Settings Panel", callback_data="settings_btn"),
                InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
            ],
            [
                InlineKeyboardButton('📢 Channels', callback_data="channels_info"),
                InlineKeyboardButton('👨‍💻 Developers', callback_data="dev_info")
            ]
        ]
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=photo_url,
                caption=script.START_TXT.format(callback_query.from_user.mention, bot.username, bot.first_name)
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "close_btn":
        await message.delete()

    elif data in ["cmd_list_btn", "user_stats_btn", "dump_chat_btn", "thumb_btn", "caption_btn"]:
        pass

    await callback_query.answer()
