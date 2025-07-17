from minibot.network import Minibot

def start_handler(chat_id):
    buttons = [[
        {'text': 'Channel', 'url': 'https://t.me/minicoderchannel'},
        {'text': 'Button'}
    ]]
    reply_markup = bot.create_inline_keyboard(buttons)
    bot.send_message(chat_id, "Helloy my bot", reply_markup)


def help_handler(chat_id):
    help_text = (
        "comamnds:\n"
        "/start - start bot\n"
        "/help - message open \n"
    )
    bot.send_message(chat_id, help_text)

if __name__ == "__main__": 
    bot = Minibot('Token')# token @BotFather
    bot.add_handler('/start', start_handler)
    bot.add_handler('/help', help_handler)  #help  handler
    bot.start()