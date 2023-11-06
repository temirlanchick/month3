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


@questions_router.message(Command('stop'))
@questions_router.message(F.text.lower() == 'отмена')
async def stop_questions(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('До свидания!')


@questions_router.message(Command('ask'))
async def start_questions(message: types.Message, state: FSMContext):
    await message.answer('Для того, чтобы остановить опрос, напишите "отмена"')
    await message.answer('Как вас зовут?')
    await state.set_state(Questions.name)


@questions_router.message(F.text, Questions.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())

    await message.answer('Сколько вам лет?')
    await state.set_state(Questions.age)


@questions_router.message(F.text, Questions.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text.strip()
    if (not age.isdigit()):
        await message.answer('Нужно ввести только цифры')
    if (int(age) < 12 or int(age) > 99):
        await message.answer('Возраст должен быть от 12 до 99')
    else:
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Мужской"), types.KeyboardButton(text="Женский")],
            ]
        )

        await state.update_data(age=int(message.text))
        await message.answer("Какой у вас пол?", reply_markup=kb)
        await state.set_state(Questions.gender)


@questions_router.message(F.text, Questions.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text.strip()
    if gender.lower() == "мужской" or gender.lower() == "женский":
        kb = types.ReplyKeyboardRemove()
        await state.update_data(gender=gender)
        await state.set_state(Questions.country)
        await message.answer('В какой стране вы живете?', reply_markup=kb)
    else:
        await message.answer('Нужно ввести "Мужской" или "Женский"')


@questions_router.message(F.text, Questions.country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text.strip())
    await message.answer('Спасибо за опрос!')

    data = await state.get_data()
    print(data)
    # сохранить в БД - База данных

    # очистка состояния
    await state.clear()
