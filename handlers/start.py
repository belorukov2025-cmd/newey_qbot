from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Solo Quest 🧘‍♂️", callback_data="solo"),
            InlineKeyboardButton(text="Group Quest 👥", callback_data="group")
        ],
        [
            InlineKeyboardButton(text="My Points & Badges 🏆", callback_data="profile"),
            InlineKeyboardButton(text="Yesterday's Gallery 🖼️", callback_data="gallery")
        ]
    ])
    await message.answer(
        "Hi! This is Newey, your raccoon buddy from New York 🦝🌆\n"
        "Here we disconnect from the noise and enjoy parks.\n"
        "Choose below!",
        reply_markup=keyboard
    )
