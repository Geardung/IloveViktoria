import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.markdown import link

from config import TG_TOKEN

bot = Bot(token=TG_TOKEN, default=DefaultBotProperties())

dp = Dispatcher()

main_router = Router()

class MyCallback(callback_data.CallbackData, prefix="vikasex"):
    state: str


async def main() -> None:
    
    await dp.start_polling(bot)


@main_router.callback_query(MyCallback.filter(F.state == "create_new_topic"))
async def create_topic_callback(query: CallbackQuery, callback_data: MyCallback): 
    
    markup_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="GPT-4o-mini", callback_data=MyCallback(state="select_model_gpt4o-mini").pack())],
                                                            [InlineKeyboardButton(text="GPT-4o", callback_data=MyCallback(state="select_model_gpt4o").pack())],
                                                            [InlineKeyboardButton(text="Удалить чат", callback_data=MyCallback(state="delete_this_topic").pack())]])
    
    new_topic = await query.message.bot.create_forum_topic(query.message.chat.id, "Новый чат")
    
    await query.answer()
    
    msg = await query.message.bot.send_message(
        text="Солнышко, если хочешь удалить этот чат, ты можешь воспользоваться кнопкой снизу\nТакже, кнопкой можно выбрать модель для конкретного чата!",
        reply_markup=markup_keyboard,
        chat_id=query.message.chat.id,
        message_thread_id=new_topic.message_thread_id)
    
    markup_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти в новый чатик", url=msg.get_url(include_thread_id=True))]])
    
    dl_msg = await bot.send_message(query.message.chat.id, f"Солнце, {link('чатик', url=msg.get_url(include_thread_id=True) )} создан.",
                                    reply_markup=markup_keyboard,
                                    parse_mode="MARKDOWN")
    
    await asyncio.sleep(15)
    
    await dl_msg.delete()
    
    await msg.pin()
    
    
    
@main_router.message(Command("new"))
async def create_topic(message: Message):
    
    markup_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="GPT-4o-mini", callback_data=MyCallback(state="select_model_gpt4o-mini").pack())],
                                                            [InlineKeyboardButton(text="GPT-4o", callback_data=MyCallback(state="select_model_gpt4o").pack())],
                                                            [InlineKeyboardButton(text="Удалить чат", callback_data=MyCallback(state="delete_this_topic").pack())]])
    
    new_topic = await message.bot.create_forum_topic(message.chat.id, "Новый чат")
    
    msg = await message.bot.send_message(
        text="Солнышко, если хочешь удалить этот чат, ты можешь воспользоваться командой /delete\nТакже, если хочешь изменить модель для этого чата, воспользуйся кнопками ниже!",
        reply_markup=markup_keyboard,
        chat_id=message.chat.id,
        message_thread_id=new_topic.message_thread_id)
    
    await msg.pin()
    
    await message.delete()

@main_router.callback_query(MyCallback.filter(F.state == "delete_this_topic"))
async def callback_query_handler(query: CallbackQuery, callback_data: MyCallback): 
    
    await bot.delete_forum_topic(query.message.chat.id,
                                 query.message.message_thread_id)
    
@main_router.message(Command("adm-reg"))
async def deererrelete_topic(message: Message):
    
    markup_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Новый чат", callback_data=MyCallback(state="create_new_topic").pack())]])
    
    msg = await message.bot.send_message(
        text="Викуличка любимая, чтобы создать новый чат для диалога с ботом, нажми на кнопку снизу",
        reply_markup=markup_keyboard,
        chat_id=message.chat.id)
    
    await msg.pin()
    
    await message.delete()

    

@main_router.message(Command("adm-delete"))
async def delete_topic(message: Message):
    
    await bot.delete_forum_topic(message.chat.id,
                                 message.message_thread_id)


@main_router.message()
async def get_message(message: Message):
    
    pass

dp.include_router(main_router)

if __name__ == "__main__":
    
    asyncio.run(main())