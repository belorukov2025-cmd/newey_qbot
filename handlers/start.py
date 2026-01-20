from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# Состояния
class QuestStates(StatesGroup):
    main_menu = State()
    choosing_solo = State()
    active_solo = State()
    waiting_photo_solo = State()
    active_group = State()
    waiting_photo_group = State()

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

# Обработка callback
@router.callback_query()
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    state_data = await state.get_data()
    main_msg_id = state_data.get("main_msg_id")

    if main_msg_id is None:
        await cmd_start(callback.message, state)
        return

    keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
    ])

    text = ""

    if data == "solo":
        await state.set_state(QuestStates.choosing_solo)
        text = (
            "Solo Quests from Newey! 🧘‍♂️\n"
            "Choose one:\n"
            "1. Sit for 20 min on a bench by the fountain in Bryant Park 🌳🪑\n"
            "2. Walk for 15 min along High Line 🚶‍♂️🌉"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Quest 1", callback_data="solo_1")],
            [InlineKeyboardButton(text="Quest 2", callback_data="solo_2")],
            [InlineKeyboardButton(text="Back 🔙", callback_data="back")]
        ])

    elif data in ["solo_1", "solo_2"]:
        await state.set_state(QuestStates.active_solo)
        quest_num = "1" if data == "solo_1" else "2"
        await state.update_data(active_quest=quest_num)
        text = f"Solo Quest {quest_num} started! 🧘‍♂️\nDo it whenever you're ready.\nWhen finished — press 'Complete' below."
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Complete Quest 🏁", callback_data="complete_solo")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])

    elif data == "complete_solo":
        await state.set_state(QuestStates.waiting_photo_solo)
        text = (
            "Quest completed! 🎉\n"
            "Choose:\n"
            "• +5 points without photo 💰\n"
            "• +15 points with photo 📸 (send photo now)"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="+5 points 💰", callback_data="solo_5_no_photo")],
            [InlineKeyboardButton(text="+15 points with photo 📸", callback_data="solo_15_photo")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])

    elif data == "group":
        await state.set_state(QuestStates.active_group)
        text = (
            "Group Quest from Newey! 👥\n"
            "Today: 18:00–19:30 at Sheep Meadow\n"
            "Activity: 20–30 min light yoga on the grass 🧘‍♂️\n"
            "Come, chat, enjoy! When done — press 'Complete'."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Complete Quest 🏁", callback_data="complete_group")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])

    elif data == "complete_group":
        await state.set_state(QuestStates.waiting_photo_group)
        text = (
            "Group Quest completed! 🎉\n"
            "Choose:\n"
            "• +5 points without photo\n"
            "• +15 points with photo (send photo now)"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="+5 points 💰", callback_data="group_5_no_photo")],
            [InlineKeyboardButton(text="+15 points with photo 📸", callback_data="group_15_photo")],
            [InlineKeyboardButton(text="Back to Menu 🔙", callback_data="back")]
        ])

    # Обработка начисления баллов (пока просто текст)
    elif data in ["solo_5_no_photo", "solo_15_photo", "group_5_no_photo", "group_15_photo"]:
        points = 5 if "5" in data else 15
        text = f"Awesome! You earned +{points} points! 🎉\nNewey is proud of you 🦝"
        keyboard = get_main_keyboard()
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard
        )
        await state.set_state(QuestStates.main_menu)
        await state.update_data(active_quest=None)

    elif data == "profile":
        text = (
            "Your progress with Newey 🦝:\n"
            "Earned points: 0\n"
            "Completed quests: 0\n"
            "Sent photos: 0\n"
            "My badges: empty for now 😔"
        )
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard_back
        )

    elif data == "gallery":
        text = (
            "Yesterday's Gallery 🖼️\n"
            "No photos yet... Check tomorrow from other participants! 😊"
        )
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard_back
        )

    elif data == "back":
        text = "How's your day going? 🌟\nNewey is here to make it better!"
        keyboard = get_main_keyboard()
        await callback.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=main_msg_id,
            text=text,
            reply_markup=keyboard
        )
        await state.set_state(QuestStates.main_menu)

    await callback.answer()
