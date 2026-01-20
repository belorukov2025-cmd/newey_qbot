from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# Состояния для хранения message_id главного меню
class MenuStates(StatesGroup):
    main_menu = State()

# Главное меню
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
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
    sent_message = await message.answer(
        "Hi! This is Newey, your raccoon buddy from New York 🦝🌆\n"
        "Here we disconnect from the noise and enjoy parks.\n"
        "Choose below!",
        reply_markup=keyboard
    )
    # Сохраняем ID сообщения меню
    await state.set_state(MenuStates.main_menu)
    await state.update_data(main_menu_msg_id=sent_message.message_id)

# Обработка всех кнопок
@router.callback_query()
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    # Получаем ID сообщения меню, чтобы редактировать его
    data_state = await state.get_data()
    main_msg_id = data_state.get("main_menu_msg_id")

    if main_msg_id is None:
        # Если ID потерян — отправляем новое меню
        await cmd_start(callback.message, state)
        return

    text = ""
    keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
    ])

    if data == "solo":
        text = (
            "Solo Quests from Newey! 🧘‍♂️\n"
            "Here are 2 options available today:\n"
            "1. Sit for 20 min on a bench by the fountain in Bryant Park 🌳🪑\n"
            "2. Walk for 15 min along High Line 🚶‍♂️🌉\n"
            "Choose one (you can take the second after completing the first)."
        )

    elif data == "group":
        text = (
            "Group Quest from Newey! 👥\n"
            "Today: 18:00–19:30 at Sheep Meadow in Central Park\n"
            "Activity: 20–30 min light yoga on the grass 🧘‍♂️\n"
            "Come, chat, enjoy the moment!"
        )

    elif data == "profile":
        text = (
            "Your progress with Newey 🦝:\n"
            "Earned points: 0\n"
            "Completed quests: 0\n"
            "Sent photos: 0\n"
            "My badges: empty for now 😔"
        )

    elif data == "gallery":
        text = (
            "Yesterday's Gallery 🖼️\n"
            "No photos yet... Check tomorrow from other participants! 😊"
        )

    elif data == "back":
        # Возвращаем главное меню
        await callback.message.edit_text(
            "Hi! This is Newey, your raccoon buddy from New York 🦝🌆\n"
            "Here we disconnect from the noise and enjoy parks.\n"
            "Choose below!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Solo Quest 🧘‍♂️", callback_data="solo"),
                    InlineKeyboardButton(text="Group Quest 👥", callback_data="group")
                ],
                [
                    InlineKeyboardButton(text="My Points & Badges 🏆", callback_data="profile"),
                    InlineKeyboardButton(text="Yesterday's Gallery 🖼️", callback_data="gallery")
                ]
            ])
        )
        await callback.answer()
        return

    # Редактируем главное сообщение
    try:
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard_back
        )
    except:
        # Если сообщение удалено — отправляем новое
        sent = await callback.message.answer(text, reply_markup=keyboard_back)
        await state.update_data(main_menu_msg_id=sent.message_id)

    await callback.answer()
