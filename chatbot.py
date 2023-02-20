#!/usr/bin/python3
import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai_helper import ask_bot, gen_img

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

config = {
  "maxtokens": 16,
  "temperature": 1,
  "imgnum": 1,
  "imgsize": "512x512",
}

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
    chat_id=update.effective_chat.id, text=f"Prefix 'ask ' or '问 ' to your question you wanna ask to ChatGPT\nPrefix draw/画 ' to your prompt you wanna ask DALL-E to draw for you." 
  )

async def setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_text = update.message.text
  logging.info(f"Got user setting '{user_text}'")
  user_settings = re.split(r',\s*', user_text[4:])
  logging.info(user_settings)
  for us in user_settings:
    [setkey, setval] = us.split(' ')
    logging.info(f"Setting '{setkey}' : '{setval}'")
    await context.bot.send_message(
      chat_id=update.effective_chat.id, text=f"Setting '{setkey}' : '{setval}'"
    )
    if setkey == "imgsize":
      config[setkey] = setval
    elif setkey == "temperature":
      config[setkey] = float(setval)
    else:
      config[setkey] = int(setval)

async def askBot(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_text = update.message.text
  logging.info(f"Got user text '{user_text}'")
  if (user_text[0:4] == "ask "):
    user_text = user_text[4:]
    logging.info(f"User asks that '{user_text}'")
  elif (user_text[0:2] == "问 "):
    user_text = user_text[2:]
    logging.info(f"用户问：{user_text}")
  else: 
    logging.info(f"[askBot] normal message")
    return
  answer = ask_bot(user_text, max_tokens=config["maxtokens"], temperature=config["temperature"])
  logging.info(f"ChatGPT answers that '{answer}'")
  await context.bot.send_message(
    chat_id=update.effective_chat.id, text=f"{answer}"
  )

async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_text = update.message.text
  logging.info(f"Got user prompt '{user_text}'")
  if (user_text[0:5] == "draw "):
    user_text = user_text[5:]
    logging.info(f"User input prompt: '{user_text}'")
  elif (user_text[0:2] == "画 "):
    user_text = user_text[2:]
    logging.info(f"用户要画: '{user_text}'")
  else: 
    logging.info(f"[draw] normal message")
    return
  imageurls = gen_img(user_text, size=config["imgsize"], num=config["imgnum"])
  for img in imageurls:
    logging.info(f"Sending photo: {img}")
    await context.bot.send_photo(
      chat_id=update.effective_chat.id, photo=img
    )

async def show_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(
    chat_id=update.effective_chat.id, text=f"{config}"
  )

if __name__ == "__main__":
  print(os.getenv("TGBOT_KEY"))
  app = ApplicationBuilder().token(os.getenv("TGBOT_KEY")).build()

  help_hdl = CommandHandler("help", help)
  ask_hdl = MessageHandler(filters.Regex(r'^ask ') | filters.Regex(r'^问 '), askBot)
  img_hdl = MessageHandler(filters.Regex(r'^draw ') | filters.Regex(r'^画 '), draw)
  set_hdl = MessageHandler(filters.Regex(r'^set '), setting)
  showset_hdl = MessageHandler(filters.Regex(r'^showset$'), show_setting)
  app.add_handler(help_hdl)
  app.add_handler(ask_hdl)
  app.add_handler(img_hdl)
  app.add_handler(set_hdl)
  app.add_handler(showset_hdl)
  
  app.run_polling()