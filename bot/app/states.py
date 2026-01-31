from aiogram.fsm.state import State, StatesGroup

class ReviewForm(StatesGroup):
    company = State()
    position = State()
    grade = State()
    salary = State()
    recruiter_name = State()
    recruiter_contacts = State()
    screening_rating = State()
    interviewer_name = State()
    tech_rating = State()
    details = State()