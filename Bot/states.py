from aiogram.fsm.state import State, StatesGroup

class WaitCode(StatesGroup):
    reg_teacher = State()
    reg_student = State()

class AddStudent(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    kvant = State()
    level = State()
    num = State()

class GetCode(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()

class DeleteStudent(StatesGroup):
    id = State()
    name = State()
    surname = State()
    patronymic = State()