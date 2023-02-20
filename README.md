# ChatGPT-Telegram-Bot-Python
A ChatGPT Bot of Telegram in Python

It's a open-source Telegram Bot that use OpenAI GPT-3 API. The Bot has two main features:
* User can ask a question to the bot and get answer from AI ('text-davinci-003')
* User can input a prompt to the bot and get the generated image from AI (DALL-E)

## How to Use

Set the environment variable with your OpenAI API key and your telegram bot key
```bash
export TGBOT_KEY=<your telegram bot key>
export OPENAI_KEY=<your OpenAI API key>
```

Then run the chatbot with
```bash
$ screen python3 chatbot.py
```
