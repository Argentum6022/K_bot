from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from progonka import solve,temp_map,surface
import os



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

class Teploprov(StatesGroup):
    waiting_for_x = State()
    waiting_for_t = State()
    waiting_for_ft = State()
    waiting_for_zt = State()
    waiting_for_u0 = State()
    waiting_for_lam = State()


#Функция старт
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Здравстуйте, я K_Bot!"
                        " \nПри помощи меня вы можете решить уравнение теплопроводности на стержне."
                        " \nДля получения инструкции напишите /help")


#Функция окна помощи
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Для того чтобы начать сначала напишите /start "
                        "\nЧтобы снова увидеть это окно /help "
                        "\nДля поиска продукта напишите /solution")

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Для того чтобы начать работу нажмите (\solution).",
        reply_markup=types.ReplyKeyboardRemove())

async def lets_start(message: types.Message, state: FSMContext):
    await message.answer("Введите координаты стержня следующим образом: xmin,xmax,h "
                         "\n где h это шаг сетки. Длина стержня должна быть кратна шагу"
                         "\nНапример: 2,3.82,0.13 !Важно! В десятичной дроби используйте точки!", reply_markup=keyboard)
    await state.set_state(OrderFood.waiting_for_x.state)

async def x_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace(" ", "")
    x = [float(o) for o in s.split(',')]
    if x[0]>x[1] or x[2]>x[1]-x[0] or len(x)>3:
        await message.answer("Пожалуйста, проверьте правильность заполнения координат.")
        return
    await state.update_data(x_data=x)

    await state.set_state(OrderFood.waiting_for_t.state)
    await message.answer("Теперь определимся с промежутком времени: tmin,tmax,T"
                         "\n где T это шаг временной сетки. Период времени должен быть кратен шагу"
                         "\n Например: 0.02,0.14,0.01 !Важно! В десятичной дроби используйте точки!", reply_markup=keyboard)

async def t_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace(" ", "")
    t = [float(o) for o in s.split(',')]
    if t[0]>t[1] or t[2]>t[1]-t[0] or len(t) > 3:
        await message.answer("Пожалуйста, проверьте правильность заполнения временной шкалы.")
        return
    await state.update_data(t_data=t)

    await state.set_state(OrderFood.waiting_for_ft.state)
    await message.answer("Впишите левое граничное условие"
                         "\n просто напишите правую часть уравнения вида f(t)=f"
                         "\n Например: (18*t)^2+4.87 !Важно! В десятичной дроби используйте точки!", reply_markup=keyboard)

async def ft_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace("^", "**")
    s.replace(" ", "")
    s.replace("cos", "math.cos")
    s.replace("sin", "math.sin")
    s.replace("tan", "math.tan")
    s.replace("sqrt", "math.sqrt")
    s.replace("exp", "math.exp")
    ft=s
    if s.search('t', the_string)==False:
        await message.answer("Пожалуйста, проверьте правильность уравнения.")
        return
    await state.update_data(ft_data=ft)
    await state.set_state(OrderFood.waiting_for_zt.state)
    await message.answer("Впишите правое граничное условие"
                         "\n просто напишите правую часть уравнения вида z(t)=z"
                         "\n Например: 12*cos(6*t) !Важно! В десятичной дроби используйте точки!", reply_markup=keyboard)

async def zt_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace("^", "**")
    s.replace(" ", "")
    s.replace("cos", "math.cos")
    s.replace("sin", "math.sin")
    s.replace("tan", "math.tan")
    s.replace("sqrt", "math.sqrt")
    s.replace("exp", "math.exp")
    zt = s
    if s.search('t', the_string) == False:
        await message.answer("Пожалуйста, проверьте правильность уравнения.")
        return
    await state.update_data(zt_data=zt)
    await state.set_state(OrderFood.waiting_for_u0.state)
    await message.answer("Впишите начальное условие"
                         "\n просто напишите правую часть уравнения вида u0(x)=u0"
                         "\n Например: 3^(x/2)+x !Важно! В десятичной дроби используйте точки!",reply_markup=keyboard)

async def u0_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace("^", "**")
    s.replace(" ", "")
    s.replace("cos", "math.cos")
    s.replace("sin", "math.sin")
    s.replace("tan", "math.tan")
    s.replace("sqrt", "math.sqrt")
    s.replace("exp", "math.exp")
    u0 = s
    if s.search('x',the_string)==False:
        await message.answer("Пожалуйста, проверьте правильность уравнения.")
        return
    await state.update_data(u0_data=u0)
    await state.set_state(OrderFood.waiting_for_lam.state)
    await message.answer("Коэффицент тееплопроводности"
                         "\n Например: 1 !Важно! В десятичной дроби используйте точки!",
                         reply_markup=keyboard)

async def lam_chosen(message: types.Message, state: FSMContext):
    lam=float(message.text)
    if lam<0 or lam>10000:
        await message.answer("Пожалуйста, проверьте правильность коэффициента.")
        return
    user_data = await state.get_data()
    xmin = user_data['x_data[0]']
    xmax = user_data['x_data[1]']
    h = user_data['x_data[2]']
    tmax = user_data['t_data[0]']
    tmin = user_data['t_data[1]']
    T = user_data['t_data[2]']
    lam = lam

    t_list = []
    x_list = []
    f_list = []
    z_list = []
    u0_list = []
    a_list = [0]

    def u0(x):
        return eval(user_data['u0_data'])
    def ft(t):
        return eval(user_data['ft_data'])
    def zt(t):
        return eval(user_data['zt_data'])

    a=solve(xmin,xmax,h,tmin, tmax,T,lam)
    a.to_excel('solution.xlsx', sheet_name='Лист1')
    await message.document.download(destination="\K_bot\solution.xlsx")
    if os.path.isfile('\K_bot\solution.xlsx'):
        os.remove('\K_bot\solution.xlsx')
        print("success")
    else:
        print("File doesn't exists!")

    fig = temp_map(a)
    fig.show()

    sur = surface(a)
    sur.show()

    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(food_start, commands="solution", state="*")

    dp.register_message_handler(x_chosen, state=Teploprov.waiting_for_x)
    dp.register_message_handler(t_chosen, state=Teploprov.waiting_for_t)
    dp.register_message_handler(ft_chosen, state=Teploprov.waiting_for_ft)
    dp.register_message_handler(zt_chosen, state=Teploprov.waiting_for_zt)
    dp.register_message_handler(u0_chosen, state=Teploprov.waiting_for_u0)
    dp.register_message_handler(lam_chosen, state=Teploprov.waiting_for_lam)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")

