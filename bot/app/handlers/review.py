from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import ReviewForm
from app.keyboards.reply import get_main_keyboard, get_cancel_keyboard, get_rating_keyboard
from app.config import settings
from aiogram import Bot
from sqlalchemy import select

router = Router()

@router.message(F.text == "📝 Оставить отзыв")
async def start_review(message: Message, state: FSMContext):
    """Начало процесса сбора отзыва"""
    await state.set_state(ReviewForm.company)
    await message.answer(
        "📋 <b>Отзыв о процессе найма</b>\n\n"
        "Давай начнем! Ответь на несколько вопросов.\n\n"
        "1️⃣ <b>Название компании:</b>",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.company)
async def process_company(message: Message, state: FSMContext):
    """Получение названия компании"""
    await state.update_data(company=message.text)
    await state.set_state(ReviewForm.position)
    await message.answer(
        "2️⃣ <b>Название вакансии/должности:</b>\n"
        "(например: Python Backend Developer)",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.position)
async def process_position(message: Message, state: FSMContext):
    """Получение должности"""
    await state.update_data(position=message.text)
    await state.set_state(ReviewForm.grade)
    await message.answer(
        "3️⃣ <b>Грейд/уровень:</b>\n"
        "(например: Junior, Middle, Senior или оставь пустым если не знаешь)",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.grade)
async def process_grade(message: Message, state: FSMContext):
    """Получение грейда"""
    await state.update_data(grade=message.text if message.text.lower() not in ["нет", "не знаю", "-"] else None)
    await state.set_state(ReviewForm.salary)
    await message.answer(
        "4️⃣ <b>Обсуждаемая зарплата:</b>\n"
        "(например: 200k-250k RUB или оставь пустым если не озвучили)",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.salary)
async def process_salary(message: Message, state: FSMContext):
    """Получение зарплаты"""
    await state.update_data(salary=message.text if message.text.lower() not in ["нет", "не озвучили", "-"] else None)
    await state.set_state(ReviewForm.recruiter_name)
    await message.answer(
        "5️⃣ <b>Имя рекрутера:</b>\n"
        "(если помнишь)",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.recruiter_name)
async def process_recruiter_name(message: Message, state: FSMContext):
    """Получение имени рекрутера"""
    await state.update_data(recruiter_name=message.text if message.text.lower() not in ["нет", "не помню", "-"] else None)
    await state.set_state(ReviewForm.recruiter_contacts)
    await message.answer(
        "6️⃣ <b>Контакты рекрутера:</b>\n"
        "(телефон, telegram, email - что помнишь)",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.recruiter_contacts)
async def process_recruiter_contacts(message: Message, state: FSMContext):
    """Получение контактов рекрутера"""
    await state.update_data(recruiter_contacts=message.text if message.text.lower() not in ["нет", "не помню", "-"] else None)
    await state.set_state(ReviewForm.screening_rating)
    await message.answer(
        "7️⃣ <b>Оцени процесс скрининга с рекрутером:</b>\n"
        "От 1 (ужасно) до 10 (отлично)",
        parse_mode="HTML",
        reply_markup=get_rating_keyboard()
    )
@router.message(ReviewForm.screening_rating)
async def process_screening_rating(message: Message, state: FSMContext):
    """Получение оценки скрининга"""
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        await message.answer("Пожалуйста, выбери число от 1 до 10")
        return
    
    await state.update_data(screening_rating=int(message.text))
    await state.set_state(ReviewForm.interviewer_name)
    await message.answer(
        "8️⃣ <b>Имя технического интервьюера:</b>\n"
        "(если был технический этап)",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.interviewer_name)
async def process_interviewer_name(message: Message, state: FSMContext):
    """Получение имени интервьюера"""
    await state.update_data(interviewer_name=message.text if message.text.lower() not in ["нет", "не было", "-"] else None)
    await state.set_state(ReviewForm.tech_rating)
    await message.answer(
        "9️⃣ <b>Оцени процесс технического интервью:</b>\n"
        "От 1 (ужасно) до 10 (отлично)\n"
        "(или напиши '-' если не было)",
        parse_mode="HTML",
        reply_markup=get_rating_keyboard()
    )

@router.message(ReviewForm.tech_rating)
async def process_tech_rating(message: Message, state: FSMContext):
    """Получение оценки техинтервью"""
    if message.text == "-" or message.text.lower() in ["нет", "не было"]:
        await state.update_data(tech_rating=None)
    elif message.text.isdigit() and 1 <= int(message.text) <= 10:
        await state.update_data(tech_rating=int(message.text))
    else:
        await message.answer("Пожалуйста, выбери число от 1 до 10 или '-'")
        return
    
    await state.set_state(ReviewForm.details)
    await message.answer(
        "🔟 <b>Расскажи интересные подробности о процессе, чем бы тебе хотелось поделиться:</b>\n\n"
        "Что понравилось? Что не понравилось? Какие были этапы?\n"
        "Любые детали, которые помогут другим кандидатам.",
        parse_mode="HTML",
        reply_markup=get_cancel_keyboard()
    )

@router.message(ReviewForm.details)
async def process_details(message: Message, state: FSMContext, bot: Bot):
    """Финальный шаг - сохранение отзыва"""
    await state.update_data(details=message.text)
    
    # Получаем все данные
    data = await state.get_data()
    
    # Простые импорты
    from app.database import async_session_maker
    from app.models import User, Review, ReviewStatus
    
    async with async_session_maker() as db:
        # Получаем или создаем пользователя
        result = await db.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        # Создаем отзыв
        review = Review(
            user_id=user.id,
            company=data['company'],
            position=data['position'],
            grade=data.get('grade'),
            salary=data.get('salary'),
            recruiter_name=data.get('recruiter_name'),
            recruiter_contacts=data.get('recruiter_contacts'),
            screening_rating=data['screening_rating'],
            interviewer_name=data.get('interviewer_name'),
            tech_rating=data.get('tech_rating'),
            details=data['details'],
            status=ReviewStatus.PENDING
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)
        
        review_id = review.id
    
    # Уведомление админу  
    admin_message = (
        f"🆕 <b>Новый отзыв #{review_id}</b>\n\n"
        f"<b>Компания:</b> {data['company']}\n"
        f"<b>Должность:</b> {data['position']}\n"
        f"<b>Грейд:</b> {data.get('grade', 'не указан')}\n"
        f"<b>ЗП:</b> {data.get('salary', 'не указана')}\n"
        f"<b>Рекрутер:</b> {data.get('recruiter_name', 'не указан')}\n"
        f"<b>Контакты:</b> {data.get('recruiter_contacts', 'не указаны')}\n"
        f"<b>Оценка скрининга:</b> {data['screening_rating']}/10\n"
        f"<b>Интервьюер:</b> {data.get('interviewer_name', 'не указан')}\n"
        f"<b>Оценка техинтервью:</b> {data.get('tech_rating', 'не было')}/10\n\n"
        f"<b>Детали:</b>\n{data['details']}\n\n"
        f"От: @{message.from_user.username or 'anonymous'} (ID: {message.from_user.id})"
    )
    
    await bot.send_message(
        chat_id=settings.ADMIN_TELEGRAM_ID,
        text=admin_message,
        parse_mode="HTML"
    )
    
    await state.clear()
    await message.answer(
        "✅ <b>Спасибо за отзыв!</b>\n\n"
        "Твой отзыв отправлен на модерацию.\n"
        "После проверки он будет опубликован в канале.",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )