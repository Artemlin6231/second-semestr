import telegram
import config
TOKEN = config.token
bot = telegram.Bot(TOKEN)
import pycodestyle

def get_last_update_id(updates):
    """Возвращает ID последнего апдейта"""
    id_list = list()  # пустой список ID апдейтов
    for update in updates:  # для каждого апдейта
        id_list.append(update["update_id"])  # заносим в список его ID
    return (max(id_list))  # возвращаем последний


last_update_id = None
while True:
    updates = bot.getUpdates(last_update_id, timeout=100)
    if len(updates) > 0:
        last_update_id = get_last_update_id(updates) + 1
        for update in updates:  # сообщения могут приходить быстро, быстрее, чем работает код
            last_message = update["message"]  # взяли из него сообщен
            last_chat_id = last_message['chat']['id']
            fid = last_message.document.file_id
            inpfile = bot.getFile(fid)
            inpfile.download('filename.py')
            fchecker=pycodestyle.Checker('filename.py', show_source=False)
            file_errors = fchecker.check_all()
            print(file_errors)
            bot.sendMessage(last_chat_id,str(file_errors))
