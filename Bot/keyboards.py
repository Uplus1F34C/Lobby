from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def cancel_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="❌ Отменить операцию",
        callback_data="cancel_operation"))
    return builder.as_markup()

def role_selection_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="👨‍🏫 Я учитель", callback_data="role_teacher"),
        InlineKeyboardButton(text="👨‍🎓 Я ученик", callback_data="role_student")
    )
    return builder.as_markup()

def teacher_main_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="👨‍🎓 Добавить студента", callback_data="add_student"),
        InlineKeyboardButton(text="🗑️ Удалить студента", callback_data="delete_student"),
        InlineKeyboardButton(text="🔑 Получить код ученика", callback_data="get_code"),
        InlineKeyboardButton(text="🚪 Выйти из аккаунта", callback_data="exit_teacher")
    )
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()

def student_main_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📊 Отправить опрос", callback_data="post_que"),
        InlineKeyboardButton(text="💡 Предложить идею", callback_data="post_idea"),
        InlineKeyboardButton(text="📅 Узнать расписание", callback_data="schedule"),
        InlineKeyboardButton(text="🚪 Выйти из аккаунта", callback_data="exit_student")
    )
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()

def delete_method_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🔢 По ID", callback_data="delete_by_id"),
        InlineKeyboardButton(text="👤 По ФИО", callback_data="delete_by_fio"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_operation")
    )
    builder.adjust(2, 1)
    return builder.as_markup()