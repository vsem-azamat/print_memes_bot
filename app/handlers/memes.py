import asyncio
import re
from io import BytesIO

from aiogram import Router, Bot, F
from aiogram.types import Message,BufferedInputFile, FSInputFile
from aiogram.filters import Command

from app.func import edit_photo

router = Router()


@router.message(Command(commands='мем'))
# @router.message(F.photo)
async def print_memes(msg: Message, bot: Bot) -> None:
    if msg.photo:
        pattern_up = re.compile("(?<=\+\+)[\s\S]+?(?=\+\+)")
        pattern_down = re.compile("(?<=—)[\s\S]+?(?=—)")
        text_up = pattern_up.findall(msg.caption)
        text_down = pattern_down.findall(msg.caption)

        if not text_down and not text_up:
            # await msg.answer("<b>Неправильно!</b>\n\nНужно как на фото⬆️")
            await msg.reply_photo(photo=FSInputFile("./app/utils/instruction.png", "instruction"),
                                  caption=
                                  "<b>Делай как на фото</b>⬆️\n\n"\
                                  "Пример текста:\n"\
                                  "/мем"\
                                  "++ <i>Тут текст сверху</i>\n ++"\
                                  "— <i>Тут текст снизу</i> —"
                                  )

        else:
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
            memes_photo = await edit_photo(io_image=io_image, text_up=text_up, text_down=text_down)
            await msg.reply_photo(photo=BufferedInputFile(memes_photo.getbuffer().tobytes(),
                                                           filename='image_memes'))


    else:
        await msg.delete()
        msg_sent = await msg.answer("А где фото?!")
        await asyncio.sleep(30)
        await msg_sent.delete()

@router.message(F.photo)
async def test(msg: Message, bot: Bot):
    io_image = BytesIO()
    text_down = "Test up"
    text_up = """Тест Тест1 Тест2 вфыв ф вфы  
    """

    await bot.download(msg.photo[-1], io_image)
    memes_photo = await edit_photo(io_image=io_image, text_up=text_up, text_down=text_down)

    await msg.answer_photo(photo=BufferedInputFile(memes_photo.getbuffer().tobytes(),
                                                   filename='image_memes'))
