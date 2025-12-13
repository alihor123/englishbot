from aiogram.fsm.state import StatesGroup, State


class TaskState(StatesGroup):
    topic_selection = State()
    type_selection = State()
    verify = State()
