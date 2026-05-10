import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())

import os

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "clone-bot",
    api_id=11867213,
    api_hash="d475e13d8cf6937316d9fb8df5a049f9",
    bot_token="8697269007:AAFA4PRdM6bj6hN11ZWyClxBViH8fRUbUyA"
)


@app.on_message(filters.command("start"))
async def start(_, message: Message):

    await message.reply_text(
        "✅ Clone Bot Running\n\n"
        "Command:\n"
        "/clone @source @destination"
    )


@app.on_message(filters.command("clone"))
async def clone(_, message: Message):

    try:

        args = message.text.split()

        if len(args) != 3:
            return await message.reply_text(
                "Usage:\n"
                "/clone @source @destination"
            )

        source = args[1]
        destination = args[2]

        status = await message.reply_text(
            "🚀 Cloning Started..."
        )

        total = 0

        async for msg in app.get_chat_history(source):

            try:

                await app.copy_message(
                    chat_id=destination,
                    from_chat_id=source,
                    message_id=msg.id
                )

                total += 1

                if total % 50 == 0:
                    await status.edit_text(
                        f"📦 Copied: {total}"
                    )

                await asyncio.sleep(0.8)

            except FloodWait as e:

                wait_time = int(e.value)

                await status.edit_text(
                    f"⏳ FloodWait: {wait_time}s"
                )

                await asyncio.sleep(wait_time)

            except Exception as err:
                print(err)

        await status.edit_text(
            f"✅ Completed\n\n"
            f"Total Copied: {total}"
        )

    except Exception as e:
        await message.reply_text(str(e))


print("Bot Started...")
app.run()
