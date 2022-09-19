import re
import asyncio
from io import BytesIO

from aiogram import Router, Bot
from aiogram.types import Message,BufferedInputFile, FSInputFile
from aiogram.filters import Command

from app.func import edit_photo
from app.utils import text


router = Router()


@router.message(Command(commands='meme'))
async def print_memes(msg: Message, bot: Bot) -> None:
    if msg.photo:
        pattern_up = re.compile("(?<=\+\+)[\s\S]+?(?=\+\+)")
        pattern_down = re.compile("(?<=--)[\s\S]+?(?=--)")
        selected_font = re.findall(r"-f\s[AFL]", msg.caption)
        text_up = pattern_up.findall(msg.caption)
        text_down = pattern_down.findall(msg.caption)

        # If the command was incorrectly written
        if not text_down and not text_up:
            help_message = await msg.reply_photo(
                photo=FSInputFile("./app/utils/instruction.png", "instruction"),
                caption=text.text_instruction
            )
            await asyncio.sleep(20)
            await msg.delete()
            await asyncio.sleep(40)
            await help_message.delete()

        else:
            if selected_font:
                selected_font = selected_font[0][-1]
            else:
                selected_font = None
            if text_up:
                text_up = text_up[0]
            else:
                text_up = None
            if text_down:
                text_down = text_down[0]
            else:
                text_down = None
            io_image = BytesIO()
            await bot.download(msg.photo[-1], io_image)
            memes_photo = await edit_photo(io_image=io_image,
                                           text_up=text_up, text_down=text_down,
                                           selected_font=selected_font
                                           )
            await msg.reply_photo(photo=BufferedInputFile(memes_photo.getbuffer().tobytes(),
                                                           filename='image_memes'))

    else:
        await msg.delete()
        msg_sent = await msg.answer("А где фото?!")
        await asyncio.sleep(30)
        await msg_sent.delete()


@router.message(Command(commands="helpmeme"))
async def help_handler(msg: Message):
    await msg.delete()
    help_message = await msg.answer_photo(
        photo=FSInputFile("./app/utils/instruction.png", "instruction"),
        caption=text.text_instruction
    )
    await asyncio.sleep(90)
    await help_message.delete()


@router.message(Command(commands="aboutmeme"))
async def about_meme(msg: Message):
    about_message = await msg.answer(text.text_about_meme, disable_web_page_preview=True)
    await msg.delete()
    await asyncio.sleep(60)
    await about_message.delete()
