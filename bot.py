from vkbottle import Bot, Message, Proxy
from vkbottle.keyboard import Keyboard, keyboard_gen

from main import Novel
import config


class BotOutput:

    """
        Методы класса возвращают
        строку или клавиатуру 
        с ответом для пользователя.
    """

    def move(self, move: tuple):
        pass

    def generate_keyboard(self, array: list, color="secondary") -> Keyboard or False:
        if len(array) <= 5:
            # [1, 2, 3, 4, 5] => [[1], [2], [3], [4], [5]]
            return keyboard_gen([[
                {
                    "color": color,
                    "action": {
                        "type": "text",
                        "label": text,
                        "payload": str(i)
                    }
                }
            ] for i, text in enumerate(array)])
        elif len(array) <= 10:
            # [1, 2, 3, 4, 5, 6] => [[1, 2], [3, 4], [5, 6]]
            return keyboard_gen([[
                {
                    "action": {
                        "type": "text",
                        "label": text,
                        "payload": str(i)
                    },
                    "color": color
                },
                {
                    "action": {
                        "type": "text",
                        "label": array[2*i+1],
                        "payload": str(2*i+1)
                    },
                    "color": color
                }
            ] for i, text in enumerate(array[::2])])
        else:
            return False


proxy = Proxy(address="http://157.230.103.189:37826")
bot = Bot(config.token)

bot_output = BotOutput()

players = {}


@bot.on.message()
async def on_message(message: Message):
    """
        Обработчик сообщений
    """
    global players

    if message.from_id in players:
        player = players[message.from_id]
    else:
        player = players[message.from_id] = {
            "obj": Novel("Зомби апокалипсис на корабле", config.example_storyline, False, False),
            "is_choice": False
        }

    novel = player['obj']

    if player['is_choice']:
        # Проверять, является ли введенное сообщение выбором
        try:
            choice = int(message.text)
        except ValueError:
            return "Введенное значение должно быть числом!"
        else:
            len_choice = len(novel.storyline[novel.slide_id]['choice'])
            if not len_choice >= choice > 0:
                return f"Введите цифру от 1 до {len_choice}!"

        choice -= 1
        move = novel.move(choice)
        player['is_choice'] = False
    else:
        move = novel.move()

    # attachment
    attachment = None
    if 'attachment' in move:
        attachment = move['attachment']
    
    if move:
        # Если есть выбор
        if 'choice' in move:
            answer = move['text']+'\n'
            for i, option in enumerate(move['choice']):
                answer += f"\n{i+1}. {option}"

            player['is_choice'] = True
            await message(answer, attachment, keyboard=bot_output.generate_keyboard(move['choice']))
        else:
            # Возвращаем текст и аттачи
            await message(move['text'], attachment)
    else:
        return "Новелла закончена"


if __name__ == '__main__':
    bot.run_polling()
