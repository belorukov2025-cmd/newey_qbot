from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# Состояния для управления квестами и главным сообщением
class QuestStates(StatesGroup):
    main_menu = State()           # главное меню
    choosing_solo = State()       # выбор соло-квеста
    active_solo = State()         # активный соло-квест
    waiting_photo_solo = State()  # ждём фото для соло
    active_group = State()        # активный групповой квест
    waiting_photo_group = State() # ждём фото для группового

# Главное меню
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    keyboard = get_main_keyboard()
    sent = await message.answer(
        "Hi! This is Newey, your raccoon buddy from New York 🦝🌆\n"
        "Here we disconnect from the noise and enjoy parks.\n"
        "Choose below!",
        reply_markup=keyboard
    )
    await state.set_state(QuestStates.main_menu)
    await state.update_data(main_msg_id=sent.message_id)

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Solo Quest 🧘‍♂️", callback_data="solo"),
            InlineKeyboardButton(text="Group Quest 👥", callback_data="group")
        ],
        [
            InlineKeyboardButton(text="My Points & Badges 🏆", callback_data="profile"),
            InlineKeyboardButton(text="Yesterday's Gallery 🖼️", callback_data="gallery")
        ]
    ])

# Обработка всех callback-запросов
@router.callback_query()
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    state_data = await state.get_data()
    main_msg_id = state_data.get("main_msg_id")

    if main_msg_id is None:
        await cmd_start(callback.message, state)
        return

    # Базовая клавиатура "Назад"
    keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
    ])

    # --- СОЛО-КВЕСТЫ ---
    if data == "solo":
        await state.set_state(QuestStates.choosing_solo)
        text = (
            "Solo Quests from Newey! 🧘‍♂️\n"
            "Choose one (you can take the second after completing the first):\n\n"
            "1. Sit for 20 min on a bench by the fountain in Bryant Park 🌳🪑\n"
            "2. Walk for 15 min along High Line, observe the city 🚶‍♂️🌉"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Quest 1", callback_data="solo_1")],
            [InlineKeyboardButton(text="Quest 2", callback_data="solo_2")],
            [InlineKeyboardButton(text="Back 🔙", callback_data="back")]
        ])
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard
        )

    elif data in ["solo_1", "solo_2"]:
        await state.set_state(QuestStates.active_solo)
        quest_num = "1" if data == "solo_1" else "2"
        await state.update_data(active_quest=quest_num)
        text = (
            f"Solo Quest {quest_num} started! 🧘‍♂️\n"
            "Do it whenever you're ready.\n"
            "When finished — press 'Complete' below."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Complete Quest 🏁", callback_data="complete_solo")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard
        )

    elif data == "complete_solo":
        await state.set_state(QuestStates.waiting_photo_solo)
        text = (
            "Quest completed! 🎉\n"
            "Choose how to finish:\n"
            "• +5 points without photo\n"
            "• +15 points with photo (send one or more photos of the place)"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="+5 points 💰", callback_data="solo_5_no_photo")],
            [InlineKeyboardButton(text="+15 points with photo 📸", callback_data="solo_15_photo")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard
        )

    # --- ГРУППОВОЙ КВЕСТ ---
    elif data == "group":
        await state.set_state(QuestStates.active_group)
        text = (
            "Group Quest from Newey! 👥\n"
            "Today: 18:00–19:30 at Sheep Meadow in Central Park\n"
            "Activity: 20–30 min light yoga on the grass 🧘‍♂️\n"
            "Come, chat, enjoy the moment!\n"
            "When finished — press 'Complete'."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Complete Quest 🏁", callback_data="complete_group")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard
        )

    # --- ЗАВЕРШЕНИЕ КВЕСТОВ (5 или 15 баллов) ---
    elif data in ["solo_5_no_photo", "solo_15_photo", "group_5_no_photo", "group_15_photo"]:
        points = 5 if "5" in data else 15
        quest_type = "solo" if "solo" in data else "group"
        # Пока просто текст — позже добавим реальные очки
        text = f"Great job! You earned +{points} points! 🎉\nNewey is proud of you 🦝"
