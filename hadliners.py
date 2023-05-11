from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from progonka import solve,temp_map,surface
from config import TOKEN
import os
import plotly as plt



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
        "Для того чтобы начать работу нажмите (\solution).")

async def lets_start(message: types.Message, state: FSMContext):
    await message.answer("Введите координаты стержня следующим образом: xmin,xmax,h "
                         "\n где h это шаг сетки. Длина стержня должна быть кратна шагу"
                         "\nНапример: 2,3.82,0.13 !Важно! В десятичной дроби используйте точки!")
    await state.set_state(Teploprov.waiting_for_x.state)

async def x_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace(" ", "")
    x = [float(o) for o in s.split(',')]
    if x[0]>x[1] or x[2]>x[1]-x[0] or len(x)>3:
        await message.answer("Пожалуйста, проверьте правильность заполнения координат.")
        return
    await state.update_data(xmin_data=x[0])
    await state.update_data(xmax_data=x[1])
    await state.update_data(h_data=x[2])

    await state.set_state(Teploprov.waiting_for_t.state)
    await message.answer("Теперь определимся с промежутком времени: tmin,tmax,T"
                         "\n где T это шаг временной сетки. Период времени должен быть кратен шагу"
                         "\n Например: 0.02,0.14,0.01 !Важно! В десятичной дроби используйте точки!")

async def t_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s.replace(" ", "")
    t = [float(o) for o in s.split(',')]
    if t[0]>t[1] or t[2]>t[1]-t[0] or len(t) > 3:
        await message.answer("Пожалуйста, проверьте правильность заполнения временной шкалы.")
        return
    await state.update_data(tmin_data=t[0])
    await state.update_data(tmax_data=t[1])
    await state.update_data(T_data=t[2])

    await state.set_state(Teploprov.waiting_for_ft.state)
    await message.answer("Впишите левое граничное условие"
                         "\n просто напишите правую часть уравнения вида f(t)=f"
                         "\n Например: (18*t)^2+4.87 !Важно! В десятичной дроби используйте точки!")

async def ft_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s=s.replace("^", "**")
    s=s.replace(" ", "")
    s=s.replace("cos", "math.cos")
    s=s.replace("sin", "math.sin")
    s=s.replace("tan", "math.tan")
    s=s.replace("sqrt", "math.sqrt")
    s=s.replace("exp", "math.exp")
    s=s.replace("log", "math.log")
    s=s.replace(",", ".")
    ft=s
    if s.find('t')==False:
        await message.answer("Пожалуйста, проверьте правильность уравнения.")
        return
    await state.update_data(ft_data=ft)
    await state.set_state(Teploprov.waiting_for_zt.state)
    await message.answer("Впишите правое граничное условие"
                         "\n просто напишите правую часть уравнения вида z(t)=z"
                         "\n Например: 12*cos(6*t) !Важно! В десятичной дроби используйте точки!")

async def zt_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s=s.replace("^", "**")
    s=s.replace(" ", "")
    s=s.replace("cos", "math.cos")
    s=s.replace("sin", "math.sin")
    s=s.replace("tan", "math.tan")
    s=s.replace("sqrt", "math.sqrt")
    s=s.replace("exp", "math.exp")
    s=s.replace("log", "math.log")
    s=s.replace(",", ".")
    zt = s
    if s.find('t') == False:
        await message.answer("Пожалуйста, проверьте правильность уравнения.")
        return
    await state.update_data(zt_data=zt)
    await state.set_state(Teploprov.waiting_for_u0.state)
    await message.answer("Впишите начальное условие"
                         "\n просто напишите правую часть уравнения вида u0(x)=u0"
                         "\n Например: 3^(x/2)+x*log(x) !Важно! В десятичной дроби используйте точки!" )

async def u0_chosen(message: types.Message, state: FSMContext):
    s = message.text
    s=s.replace("^", "**")
    s=s.replace(" ", "")
    s=s.replace("cos", "math.cos")
    s=s.replace("sin", "math.sin")
    s=s.replace("tan", "math.tan")
    s=s.replace("sqrt", "math.sqrt")
    s=s.replace("exp", "math.exp")
    s=s.replace("log", "math.log")
    s=s.replace(",", ".")
    u0 = s
    if s.find('x')==False:
        await message.answer("Пожалуйста, проверьте правильность уравнения.")
        return
    await state.update_data(u0_data=u0)
    await state.set_state(Teploprov.waiting_for_lam.state)
    await message.answer("Коэффицент тееплопроводности"
                         "\n Например: 1 !Важно! В десятичной дроби используйте точки!")

async def lam_chosen(message: types.Message, state: FSMContext):
    lam=float(message.text)
    if lam<0 or lam>10000:
        await message.answer("Пожалуйста, проверьте правильность коэффициента.")
        return
    user_data = await state.get_data()
    xmin = user_data['xmin_data']
    xmax = user_data['xmax_data']
    h = user_data['h_data']
    tmax = user_data['tmax_data']
    tmin = user_data['tmin_data']
    T = user_data['T_data']
    lam = lam

    a=solve(xmin,xmax,h,tmin, tmax,T,lam,user_data)
    a.to_excel('solution.xlsx', sheet_name='Лист1')
    fig = temp_map(a)
    fig.write_html("map_temp.html")
    sur = surface(a)
    sur.write_html("surface.html")


    if os.path.isfile('\K_bot\solution.xlsx'):
        await message.answer_document(open("solution.xlsx",'rb'))
        await message.answer_document(open("map_temp.html",'rb'))
        await message.answer_document(open("surface.html",'rb'))
        await message.answer("Готово! Наслаждайтесь!")
        os.remove('\K_bot\solution.xlsx')
        os.remove('\K_bot\map_temp.html')
        os.remove('\K_bot\surface.html')
        print("success")
    else:
        print("File doesn't exists!")



    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(lets_start, commands="solution", state="*")

    dp.register_message_handler(x_chosen, state=Teploprov.waiting_for_x)
    dp.register_message_handler(t_chosen, state=Teploprov.waiting_for_t)
    dp.register_message_handler(ft_chosen, state=Teploprov.waiting_for_ft)
    dp.register_message_handler(zt_chosen, state=Teploprov.waiting_for_zt)
    dp.register_message_handler(u0_chosen, state=Teploprov.waiting_for_u0)
    dp.register_message_handler(lam_chosen, state=Teploprov.waiting_for_lam)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")


