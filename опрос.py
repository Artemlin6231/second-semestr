import config
import random

TOKEN = config.token

import logging # импортируем логи

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update # Update - уже рассматривали
# Также импортируем кнопки
from telegram.ext import ( # дополнительно импортируем обработчик бесед
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Вкл. логи
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
Character,TASTE, COLOR, Weapon = range(4)
Hero=['Michelangelo','Leonardo','Donatello', 'Rafael']



def start(update: Update, context: CallbackContext) -> int: # возвращает целое число
    """спрашивает каким ты себя видишь"""
    reply_keyboard = [['Strong', 'Clever', 'Angry','Funny']] # четыре кнопки в ряд

    update.message.reply_text(
        'Who are you?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return Character


def character(update: Update, context: CallbackContext) -> int:
    """Записывает характер в лог, спрашивает фото"""
    user = update.message.from_user # извлекли информацию о пользователе
    logger.info("Character of %s: %s", user.first_name, update.message.text) # записали в лог
    reply_keyboard = [['Pizza', 'Wok', 'Burger', 'Chicken']]
    update.message.reply_text( # отправляем сообщение
        'I see! What food do you prefer?',

        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return TASTE


def taste(update: Update, context: CallbackContext) -> int:
    """Сохраняет фото и спрашивает место"""
    user = update.message.from_user # извлекли информацию о пользователе
    logger.info("Photo of %s: %s", user.first_name,update.message.text) # записали в лог
    reply_keyboard = [['Blue', 'Purple', 'Red', 'Orange']]
    update.message.reply_text(
        'Gorgeous! Now, send me your favourite color!',

         reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return COLOR





def color(update: Update, context: CallbackContext) -> int:
    """Сохраняем место и спрашиваем статус"""
    user = update.message.from_user
    logger.info(
        "Color of %s: %f / %f", user.first_name, update.message.text)
    reply_keyboard = [['katana', 'stick', 'dagger', 'nunchucks']]

    update.message.reply_text(
        'Maybe I can visit you sometime! ' 'At last, tell me something about weapon that you like.',

         reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),

    )

    return Weapon




def weapon(update: Update, context: CallbackContext) -> int:
    """Получаем статус, сохраняем и прощаемся"""
    user = update.message.from_user
    logger.info("Weapon of %s: %s", user.first_name, update.message.text)
    a = random.randint(1, 5)
    update.message.reply_text('You are '+Hero[a])

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Пишем в лог завершение разговора и прощаемся"""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    a=random.randint(1,5)
    update.message.reply_text(
        'You are '+Hero[a], reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Передаём токен в Updater.
    updater = Updater(TOKEN)

    # Используем диспетчер для обработчиков
    dispatcher = updater.dispatcher

    # Добавляем обработчки беседы с состояниями GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={ # Сопоставляем состояниям значения
          Character: [MessageHandler(Filters.regex('^(Strong|Clever|Angry|Funny)$'),character)],
          TASTE: [MessageHandler(Filters.regex('^(Pizza|Wok|Burger|Chicken)$'),taste)],
          COLOR: [MessageHandler(Filters.regex('^(Blue|Purple|Red|Orange)$'),color)],
          Weapon: [MessageHandler(Filters.regex('^(katana|stick|dagger|nunchucks)$'),weapon)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler) # добавили обработчик беседы

    # Запустили бот
    updater.start_polling()

    # Бот работает до Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
