import asyncio, openai, ujson, base64, markdown
from telegraph import Telegraph
from random import randint
from datetime import datetime

from init import THREADS_FOLDER_PATH, TEMP_FOLDER_PATH

from aiogram import Bot, Dispatcher, html, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, callback_data
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReactionTypeEmoji
from aiogram.utils.markdown import link
from aiogram.utils import chat_action

import asyncio
from openai_streaming import process_response
from typing import AsyncGenerator

from config import TG_TOKEN, GPT_TOKEN, TELEGRAPH_TOKEN

tg_paginator = Telegraph(TELEGRAPH_TOKEN)

bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
main_router = Router()


client = openai.AsyncOpenAI(
    api_key=GPT_TOKEN,
    base_url="https://bothub.chat/api/v2/openai/v1"
)

anthr_client = openai.AsyncOpenAI(
    api_key=GPT_TOKEN,
    base_url="https://bothub.chat/api/v2/openai/v1"
)




class MyCallback(callback_data.CallbackData, prefix="vikasex"):
    state: str

async def main() -> None: await dp.start_polling(bot)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@main_router.callback_query(MyCallback.filter(F.state == "create_new_topic"))
async def create_topic_callback(query: CallbackQuery, callback_data: MyCallback): 
    
    markup_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="GPT-4o-mini", callback_data=MyCallback(state="select_model_gpt4o-mini").pack())],
                                                            [InlineKeyboardButton(text="GPT-4o", callback_data=MyCallback(state="select_model_gpt4o").pack())],
                                                            [InlineKeyboardButton(text="Удалить чат", callback_data=MyCallback(state="delete_this_topic").pack())]])
    
    new_topic = await query.message.bot.create_forum_topic(query.message.chat.id, "Новый чат")
    
    await query.answer()
    
    with open(THREADS_FOLDER_PATH + str(new_topic.message_thread_id) + ".json", "w", encoding="utf-8") as f:
        
        f.write(ujson.dumps({
            "engine-selected-now": "gpt-4o"
        }))
        
    
    msg = await query.message.bot.send_message(
        text="Солнышко, если хочешь удалить этот чат, ты можешь воспользоваться кнопкой снизу\nТакже, кнопкой можно выбрать модель для конкретного чата!",
        reply_markup=markup_keyboard,
        chat_id=query.message.chat.id,
        message_thread_id=new_topic.message_thread_id)
    
    markup_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти в новый чатик", url=msg.get_url(include_thread_id=True))]])
    
    dl_msg = await bot.send_message(query.message.chat.id, f"Солнце, {link('чатик', url=msg.get_url(include_thread_id=True) )} создан.",
                                    reply_markup=markup_keyboard,
                                    parse_mode="MARKDOWN")
    
    await asyncio.sleep(5)
    
    await dl_msg.delete()
    
    await msg.pin()

@main_router.callback_query(MyCallback.filter(F.state == "delete_this_topic"))
async def callback_query_handler(query: CallbackQuery, callback_data: MyCallback): 
    
    await bot.delete_forum_topic(query.message.chat.id,
                                 query.message.message_thread_id)
    
@main_router.message(Command("adm-thread-id"))
async def delete_topic(message: Message):
    
    await message.reply(
        f"{message.message_thread_id}"
                        )

@main_router.message()
async def any_topic_message(message: Message):
    
    def replace_markdownv2(text: str):
        
        n = text
        
        for _ in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
            
            n = n.replace(_, f"\{_}")
            
        return n
    
    
    if not message.chat.is_forum: return
    elif message.message_thread_id in [None, 3]: return
    elif message.from_user.is_bot: return
    
    
    #with open(THREADS_FOLDER_PATH + )
    
    
    await bot.send_chat_action(chat_id=message.chat.id,
                         action="typing",
                         message_thread_id=message.message_thread_id,
                         )
    
    if message.photo:
    
        # photo_pathes = []
        photo_path = TEMP_FOLDER_PATH+str(randint(0, 9999999999))+"_"+str(int(datetime.now().timestamp())) + "_" + str(message.message_thread_id) + ".jpg"
        # photo_pathes.append(_)
        await bot.download(message.photo[-1], photo_path)
            # 
        # print(photo_pathes)
            # 
        # photo_promt = [{"type": "image_url", 
                        # "image_url": {"url": f"data:image/jpeg;base64,{encode_image(img)}"}} for img in photo_pathes]
    
    
    async def content_handler(content: AsyncGenerator[str, None]):
        
        n_msg = None
        
        cache = []
        
        old_message = ""
        
        async for token in content:
            
            if len(cache) >= 60: 
            
                print(old_message + replace_markdownv2("".join(cache)), end="\n----------\n")
            
                if not n_msg: n_msg = await message.reply("".join(cache), parse_mode="Markdown")
                else: n_msg = await n_msg.edit_text( old_message + "".join(cache), parse_mode="Markdown")
                
                old_message = old_message + "".join(cache)
                
                cache = []
                
            else: cache.append(token)

        if cache != []: 
            if not n_msg: n_msg = await message.reply("".join(cache), parse_mode="Markdown")
            else: await n_msg.edit_text(old_message + "".join(cache), parse_mode="Markdown")
            cache = []
            old_message = old_message + "".join(cache)
        
        await bot.set_message_reaction(message.chat.id,
                                n_msg.message_id,
                                [ReactionTypeEmoji(emoji="🤷‍♀")]
                                )
        
        
        #resp = await client.chat.completions.create(
        #    model="gpt-4o-mini",
        #    messages=[
        #        {"role": "assistant", "content": old_message},
        #        {"role": "user", "content": "Дай название чату"}]
        #)
        
    
    promt = [{"role": "system", "content": "Ты ассистент, который помогает выполнять домашнее задание из Университета. Пользуйся разметкой Markdown. Печатай правильно на Русском языке"}]
    
    
    
    
    
    
    #TODO захуярить память
    
    
    
    
    
    
    promt.append({"role": "user", "content": [{"type": "text", "text": message.text or message.caption or ("Проанализируй картинку и составь полный ответ" if message.photo else None)}]})
    
    if message.photo: promt[-1]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(photo_path)}"}})
    
    print(promt)
    
    resp = await client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=promt,
        temperature=0.2,
        max_tokens=50000,
        stream=True
    )
    
    await process_response(resp, content_handler)
    

dp.include_router(main_router)

if __name__ == "__main__":
    
    asyncio.run(main())