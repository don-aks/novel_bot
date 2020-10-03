from time import sleep

from vkbottle import Bot, Message, Proxy
from vkbottle.keyboard import Keyboard, keyboard_gen

from main import Novel
import config


class BotOutput:
    """
        Класс предназначен для
        взаимодействия с игроком.
        Здесь вся логика бота.
        Методы возвращают словарь с
        новым сообщением юзеру.
    """

    def __init__(self):
        self.players = {}

    def on_message(self, message: Message) -> dict:
        """
            Главный метод.
            Анализирует сообщение пользователя
            message и на основе него вызывает
            метод для ответа.
            :return: dict answer
        """
        player = self.__get_player_info(message.from_id)
        if player['section'] == 'game' or message.payload == '"game"':
            player['section'] = 'game'
            return self.__game_step(message, player)
        elif player['section'] == 'menu' or message.payload == '"menu"':
            player['section'] = 'menu'
            return self.__show_menu(message, player)

    def __get_player_info(self, vk_id: int) -> dict:
        """
            Возвращает информацию об игроке
            в словаре self.players.
            Если игрока нет, создает его.

            :param vk_id: player id in vk
            :return: dict player from self.players
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
                "section": "menu"
            }
            return player

    def __show_menu(self, message: Message, player: dict) -> dict:
        """
            Возвращает интерфейс меню.
            :param message: Message
            :param player: element self.players
            :return: output message
        """
        if message.text == "!play":
            player['section'] = 'game'
            return self.__game_step(message, player)
        return {
                "text": "Меню.\n" +
                "Используйте клавиатуру " +
                "или текстовые команды:\n" +
                "!play - Играть.",

                "keyboard": keyboard_gen([[
                    {
                        "text": "Играть!",
                        "color": "positive",
                        "payload": '"game"'
                    }
                ]])
        }

    def __game_step(self, message: Message, player: dict) -> dict:
        """
            Шаг вперед в новелле для
            игрока player.
            :param message: Message
            :param player: element self.players
            :return: output message
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
                    return {
                        "text": "Введите число или используйте клавиатуру!"
                    }
                else:
                    len_choice = len(novel.storyline[novel.slide_id]['choice'])
                    if not len_choice >= choice > 0:
                        return {
                            "text": f"Введите число от 1 до {len_choice}" +
                            "или используйте клавиатуру!"
                        }

                choice -= 1

            move = novel.step(choice)
            player['is_choice'] = False
        else:
            if message.payload == '"restart"' or message.text == "!restart":
                novel.slide_id = 0
            # Menu
            elif message.payload == '"menu"' or message.text == "!menu":
                player['section'] = 'menu'
                return self.__show_menu(message, player)
            move = novel.step()

        if move:
            attachment = move.get('attachment')
            # Если есть выбор
            if 'choice' in move:
                answer = move['text']+'\n'
                for i, option in enumerate(move['choice']):
                    answer += f"\n{i+1}. {option}"

                player['is_choice'] = True
                return {
                    "text": answer,
                    "keyboard": self.__generate_choice_keyboard(move['choice']),
                    "attachment": attachment
                }

            else:
                # Возвращаем текст и аттачи
                return {
                    "text": move['text'],
                    "keyboard": keyboard_gen(
                        [[
                            {'text': "Дальше ➡", "color": "primary"}
                        ]]
                    ),
                    "attachment": attachment
                }

        else:
            return {
                        "text": "Новелла закончена.\n" +
                        "Используйте клавиатуру " +
                        "или текстовые команды: \n" +
                        "!restart - Перезапустить новеллу.\n" +
                        "!menu - Выход в меню.",

                        "keyboard": keyboard_gen(
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
                    }

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
            :return: object Keyboard
                      or False if len(array) > 10
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

    def __set_activity(self, message: Message, activity="typing"):
        return message.api.request(
            'messages.setActivity',
            {
                'type': activity,
                'user_id': message.from_id
            }
        )


proxy = Proxy(address="http://165.22.64.68:37499")
vk_bot = Bot(config.token)
bot_out = BotOutput()


@vk_bot.on.message()
async def on_message(message: Message):
    """
        Когда приходит новое сообщение,
        вызывает метод on_message класса BotOutput
        и отсылает пользователю что получил.
    """

    ans = bot_out.on_message(message)

    await message(
        ans.get('text'),
        ans.get('attachment'),
        keyboard=ans.get('keyboard')
    )

if __name__ == '__main__':
    vk_bot.run_polling()
