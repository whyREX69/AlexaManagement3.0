import io
import textwrap
from PIL import Image, ImageDraw, ImageFont
from RocksAlexaRobot.events import register
import random
from RocksAlexaRobot import LOGGER, pgram as pbot
from telethon import types
from telethon.tl import functions

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await pbot(functions.channels.GetParticipantRequest(chat, user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)
        )
    elif isinstance(chat, types.InputPeerChat):

        ui = await pbot.get_peer_id(user)
        ps = (await pbot(functions.messages.GetFullChatRequest(chat.chat_id))) \
            .full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator)
        )
    else:
        return None

@register(pattern="^/sticklet (.*)")
async def sticklet(event):
    if event.is_group:
     if not (await is_register_admin(event.input_chat, event.message.sender_id)):
       return
    sticklet = event.pattern_match.group(1)
    if not sticklet:
    	get = await event.get_reply_message()
    	sticklet = get.text
    if not sticklet:
    	await event.reply("`I need text to make sticker !`")
    	return
    sticklet = textwrap.wrap(sticklet, width=10)
    sticklet = '\n'.join(sticklet)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    font = ImageFont.truetype("./RocksAlexaRobot/resources/default.ttf", size=fontsize)
    while draw.multiline_textsize(sticklet, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype("./RocksAlexaRobot/resources/default.ttf", size=fontsize)
    width, height = draw.multiline_textsize(sticklet, font=font)
    gg = ["red", "blue", "green", "yellow", "orange", "violet", "indigo"]
    hh = random.choice(gg)
    range = f"{hh}"
    draw.multiline_text(((512-width)/2,(512-height)/2), sticklet, font=font, fill=range)
    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    await event.pbot.send_file(event.chat_id, image_stream)
    
    
__help__ = """
You have a message and you want to say it as plainly as possible.

It doesn't matter if your message is a joke, showing support, political opinion, or absolute
nonsense - all you need to do to make a sticker is pick a design and type your message. It's that easy!

*Only one command:*
- `/sticklet`*:* Make text stickers with your bot.
"""

__mod_name__ = "😛 ᴛxᴛsᴛɪᴄᴋᴇʀ"