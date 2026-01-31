from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.keyboards.reply import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()
    
    await message.answer(
        "👋 Привет! Я бот для сбора отзывов о процессе найма в IT-компаниях.\n\n"
        "Здесь ты можешь анонимно поделиться своим опытом прохождения собеседований.\n\n"
        "Помни - что каждый опыт субъективен и мы всего лишь делимся информацией, которую невозможно верифицировать\n\n"
        "Нажми 📝 Оставить отзыв, чтобы начать.",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):   
    """Обработчик команды /help"""
    await message.answer(
        "ℹ️ <b>Как пользоваться ботом:</b>\n\n"
        "1️⃣ Нажми 📝 Оставить отзыв\n"
        "2️⃣ Ответь на вопросы о процессе найма\n"
        "3️⃣ Твой отзыв пройдет модерацию и будет опубликован\n\n"
        "<b>Твои данные:</b>\n"
        "• Отзывы анонимные\n"
        "• Мы не публикуем твой Telegram\n"
        "• Все данные защищены\n\n"
        "Вопросы? Напиши @admin_username",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("cancel"))
@router.message(F.text == "❌ Отменить")
async def cmd_cancel(message: Message, state: FSMContext):
    """Отмена текущего действия"""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            "Нечего отменять 🤷‍♂️",
            reply_markup=get_main_keyboard()
        )
        return
    
    await state.clear()
    await message.answer(
        "❌ Действие отменено",
        reply_markup=get_main_keyboard()
    )