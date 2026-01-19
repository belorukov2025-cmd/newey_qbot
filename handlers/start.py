from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
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

@router.callback_query()
async def handle_callback(callback: CallbackQuery):
    data = callback.data

    if data == "solo":
        await callback.message.edit_text(
            "Solo Quests from Newey! 🧘‍♂️\n"
            "Here are 2 options available today:\n"
            "1. Sit for 20 min on a bench by the fountain in Bryant Park 🌳🪑\n"
            "2. Walk for 15 min along High Line 🚶‍♂️🌉\n"
            "Choose one (you can take the second after completing the first).",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
            ])
        )

    elif data == "group":
        await callback.message.edit_text(
            "Group Quest from Newey! 👥\n"
            "Today: 18:00–19:30 at Sheep Meadow in Central Park\n"
            "Activity: 20–30 min light yoga on the grass 🧘‍♂️\n"
            "Come, chat, enjoy the moment!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
            ])
        )

    elif data == "profile":
        await callback.message.edit_text(
            "Your progress with Newey 🦝:\n"
            "Earned points: 0\n"
            "Completed quests: 0\n"
            "Sent photos: 0\n"
            "My badges: empty for now 😔",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
            ])
        )

    elif data == "gallery":
        await callback.message.edit_text(
            "Yesterday's Gallery 🖼️\n"
            "No photos yet... Check tomorrow from other participants! 😊",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
            ])
        )

    elif data == "back":
        await cmd_start(callback.message)  # return to main menu

    await callback.answer()  # remove loading clock on button
