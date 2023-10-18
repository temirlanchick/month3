from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


# FSM
# Finite State Machine - Конечный автомат
class Questions(StatesGroup):
    name = State()
    age = State()
    gender = State()
    country = State()


questions_router = Router()


@questions_router.message(Command('ask'))
async def start_questions(message: types.Message, state: FSMContext):
    await message.answer('Как вас зовут?')
    await state.set_state(Questions.name)
