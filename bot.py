from time import sleep

from vkbottle import Bot, Message, Proxy
from vkbottle.keyboard import Keyboard, keyboard_gen

from main import Novel
import config


class BotOutput:
    players = {}

    def on_message(self, message: Message) -> tuple:
        player = self.__get_player_info(message.from_id)
        if player['state'] == 'game' or message.payload == '"game"':
            player['state'] = 'game'
            return self.move(message, player)
        elif player['state'] == 'menu' or message.payload == '"menu"':
            player['state'] = 'menu'
            return self.show_menu(message, player)

    def show_menu(self, message: Message, player: dict) -> tuple:
        if message.text == "!play":
            player['state'] = 'game'
            return self.move(message, player)
        return (
                "Меню.\n" +
                "Используйте клавиатуру " +
                "или текстовые команды:\n" +
                "!play - Играть.",
                keyboard_gen([[
                    {
                        "text": "Играть!",
                        "color": "positive",
                        "payload": '"game"'
                    }
                ]])
        )

    def move(self, message: Message, player: dict) -> tuple:
        """
            Шаг вперед в новелле для
            игрока, отправивший message
        """
        player = self.__get_player_info(message.from_id)
        novel = player['obj']

        if player['is_choice']:
            if message.payload is not None:
                choice = int(message.payload) - 1
            else:
                # Проверять, является ли введенное
                # сообщение выбором.
                try:
                    choice = int(message.text)
                except ValueError:
                    return (
                        "Введите число или используйте клавиатуру!"
                    )
                else:
                    len_choice = len(novel.storyline[novel.slide_id]['choice'])
                    if not len_choice >= choice > 0:
                        return (
                            f"Введите число от 1 до {len_choice}"+
                            "или используйте клавиатуру!"
                        )

                choice -= 1

            move = novel.move(choice)
            player['is_choice'] = False
        else:
            if message.payload == '"restart"' or message.text == "!restart":
                novel.slide_id = 0
            # Menu
            elif message.payload == '"menu"' or message.text == "!menu":
                player['state'] = 'menu'
                return self.show_menu(message, player)
            move = novel.move()

        if move:
            attachment = None
            if 'attachment' in move:
                attachment = move['attachment']
            # Если есть выбор
            if 'choice' in move:
                answer = move['text']+'\n'
                for i, option in enumerate(move['choice']):
                    answer += f"\n{i+1}. {option}"

                player['is_choice'] = True
                return (
                    answer,
                    self.__generate_choice_keyboard(move['choice']),
                    attachment
                )
            else:
                # Возвращаем текст и аттачи
                return (
                    move['text'],
                    keyboard_gen(
                        [[
                            {'text': "Дальше ➡", "color": "primary"}
                        ]]
                    ),
                    attachment
                )
        else:
            return ("Новелла закончена.\n" +
                    "Используйте клавиатуру " +
                    "или текстовые команды: \n" +
                    "!restart - Перезапустить новеллу.\n" +
                    "!menu - Выход в меню.",
                    keyboard_gen(
                        [
                            [{
                                "text": "Начать заново",
                                "payload": '"restart"',
                                "color": "positive"
                            }],
                            [{
                                "text": "В меню",
                                "payload": '"menu"',
                                "color": "negative"
                            }]
                        ]
                    )
                    )

    def __generate_choice_keyboard(self,
                                   array: list,
                                   color="secondary") -> Keyboard or False:
        """
            Функция генерирует клавиатуру
            из массива выбора.
            Если элементов 5 или меньше - отводит
            каждому по 1 строке.
            Если больше, отводит макс. 2 элемента
            на строку.
            Длинна массива не больше 10.

            :param array: array choices
            :param color: color buttons
            :returns: object Keyboard or False
                      if len(array) > 10
        """
        if len(array) <= 5:
            # [1, 2, 3, 4, 5] => [[1], [2], [3], [4], [5]]

            return keyboard_gen([
                [{"text": text, "payload": str(i+1), "color": color}]
                for i, text in enumerate(array)]
            )
        elif len(array) <= 10:
            # [1, 2, 3, 4, 5, 6, 7] => [[1, 2], [3, 4], [5, 6], [7]]

            if len(array) % 2 != 0:  # нечетное
                # Добавляем, чтобы массив делился на 2
                array.append(None)

            return keyboard_gen(
                [
                    [
                        {"text": text, "payload": str(i+1), "color": color},
                        {"text": array[2*i+1], "payload": str(2*i+2), "color": color}
                    ]
                    # Если следующий элемент не добавлен искусственно выше,
                    # добавляем его в список.
                    if array[2*i+1] is not None

                    else [
                        {"text": text, "payload": str(i+1), "color": color}
                    ]
                    for i, text in enumerate(array[::2])
                ]
            )
        else:
            return False

    def __get_player_info(self, vk_id: int) -> dict:
        """
            Возвращает информацию об игроке.
            Если игрока нет, создает.

            :param vk_id: player id in vk
            :returns: dict player from self.players
        """
        if vk_id in self.players:
            return self.players[vk_id]
        else:
            player = self.players[vk_id] = {
                "obj": Novel(
                    "Зомби апокалипсис на корабле",
                    config.example_storyline, False, False
                ),
                "is_choice": False,
                "state": "menu"
            }
            return player

    def __set_activity(self, message: Message, activity="typing"):
        return message.api.request(
            'messages.setActivity',
            {
                'type': activity,
                'user_id': message.from_id
            }
        )


proxy = Proxy(address="http://192.252.223.147:3128")
bot = Bot(config.token)
bot_out = BotOutput()


@bot.on.message()
async def on_message(message: Message) -> str or None:
    """Handler VK messages"""

    answer = bot_out.on_message(message)

    text = None
    keyboard = None
    attachment = None

    if len(answer) == 0:
        return False
    if len(answer) >= 1:
        text = answer[0]
    if len(answer) >= 2:
        keyboard = answer[1]
    if len(answer) >= 3:
        attachment = answer[2]

    await message(text, attachment, keyboard=keyboard)

if __name__ == '__main__':
    bot.run_polling()
