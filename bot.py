from typing import Any, Dict, List, Optional, Union
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
        self.novels = []
        # test novel
        self.novels.append({
            "name": "Зомби-апокалипсис на корабле",
            "descr": "Вы просыпаетесь на корабле и вдруг...",
            "genre": "Зомби",
            "storyline": config.example_storyline,
            "author_id": 248015237,
            "url": "test",
            "img": "photo-29559271_456242468",
            "is_public": True,
            "is_hentai": False,
            "is_input_username": True,
            "typing_delay": 0.3
        })

    def on_message(
        self,
        message: Message
    ) -> Dict[str, Union[str, Keyboard, None]]:
        """
            Главный метод.
            Анализирует сообщение пользователя
            message и на основе него вызывает
            метод для ответа.
            :return: словарь с методами сообщения
        """
        player = self.__get_player_info(message.from_id)

        # Analyse message
        if message.payload:
            # Удаляем кавычки,
            # так как payload принимает только json.
            message.payload = message.payload.replace('"', '')

            # Если payload это вызов секции
            if message.payload in ('game', 'menu', 'editor', 'settings'):
                if player['section'] == 'game':
                    self.__remove_player_game_flags(player)
                player['section'] = message.payload
        elif message.text in ('!game', '!menu', '!editor', '!settings'):
            if player['section'] == 'game':
                self.__remove_player_game_flags(player)
            player['section'] = message.text.replace('!', '')

        # Call methods
        if player['section'] == 'game':
            return self.__game_step(message, player)
        elif player['section'] == 'menu':
            return self.__show_menu(message, player)
        elif player['section'] == 'editor':
            return self.__novel_editor(message, player)
        elif player['section'] == 'settings':
            return self.__show_settings(message, player)

    def __get_player_info(
        self,
        vk_id: int
    ) -> Dict[str, Union[str, Keyboard, None]]:
        """
            Возвращает информацию об игроке
            в словаре self.players.
            Если игрока нет, создает его.

            :param vk_id: id в vk игрока
            :return: подсловарь player
                     из словаря self.players
        """
        if vk_id in self.players:
            return self.players[vk_id]
        else:
            player = self.players[vk_id] = {
                "section": "menu",  # str
                "storyline_in_editor": None,  # list
                "own_novels_id": None,  # int
                "game_novel_id": None,  # int
                "game_slide_id": 0,     # int
                "game_vars": None,      # dict

                # Params not for BD
                "game_obj": None,  # Novel
                "game_is_choice": False,  # bool
                "game_is_input_username": False  # bool
            }
            return player

    def __show_menu(
        self,
        message: Message,
        player: Dict[str, Any]
    ) -> Dict[str, Union[str, Keyboard, None]]:
        """
            Возвращает интерфейс меню.
            :param message: Message
            :param player: element self.players
            :return: output message
        """
        return {
                "text": "Меню.\n" +
                "Используйте клавиатуру " +
                "или текстовые команды:\n" +
                "!game - Играть.\n" +
                "!editor - Редактор новелл.\n" +
                "!settings - Настройки.",

                "keyboard": keyboard_gen([
                    [{
                        "text": "🎮 Играть!",
                        "color": "positive",
                        "payload": '"game"'
                    }],
                    [
                        {
                            "text": "✏ Редактор",
                            "color": "negative",
                            "payload": '"editor"'
                        },
                        {
                            "text": "⚙ Настройки",
                            "color": "secondary",
                            "payload": '"settings"'
                        }
                    ]
                ])
        }

    def __game_step(
        self,
        message: Message,
        player: Dict[str, Any]
    ) -> Dict[str, Union[str, Keyboard, None]]:
        """
            Шаг вперед в новелле для
            игрока player.
            :param message: Message
            :param player: element self.players
            :return: output message
        """
        player = self.__get_player_info(message.from_id)
        # Не выбрана новелла
        if player['game_novel_id'] is None:
            # Перейти в каталог.
            player['game_novel_id'] = 0

        novel_dict = self.novels[player['game_novel_id']]

        # Не создан объект новеллы
        if player['game_obj'] is None:
            player['game_obj'] = Novel(
                novel_dict['storyline'],
                player['game_slide_id'],
                novel_dict['is_input_username']
            )

            novel = player['game_obj']

            # Добавляем все переменные в объект
            if isinstance(player['game_vars'], dict):
                for key, value in player['game_vars'].items():
                    if key == 'choice':
                        player['game_obj'].player_choices = value
                    elif key == 'username':
                        player['game_obj'].username = value
                    else:
                        player['game_obj'].vars[key] = value

        novel = player['game_obj']

        if novel.slide_id == 0 and novel.is_input_username:
            if player['game_is_input_username']:
                novel.username = message.text
            else:
                player['game_is_input_username'] = True
                return {
                    "text": "Введи свое имя:",
                    "keyboard": keyboard_gen([])
                }

        if player['game_is_choice']:
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

            step = novel.step(choice)
            player['game_is_choice'] = False
        else:
            if message.payload == 'restart' or message.text == "!restart":
                novel.slide_id = 0
            step = novel.step()

        if step:
            attachment = step.get('attachment')
            # Если есть выбор
            if 'choice' in step:
                answer = step['text']+'\n'
                for i, option in enumerate(step['choice']):
                    answer += f"\n{i+1}. {option}"

                player['game_is_choice'] = True
                return {
                    "text": answer,
                    "keyboard": self.__generate_choice_keyboard(step['choice']),
                    "attachment": attachment,
                    "typing_delay": novel_dict['typing_delay']
                }

            else:
                # Возвращаем текст и аттачи
                return {
                    "text": step['text'],
                    "keyboard": keyboard_gen(
                        [[
                            {'text': "Дальше ➡", "color": "primary"}
                        ]]
                    ),
                    "attachment": attachment,
                    "typing_delay": novel_dict['typing_delay']
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

    def __novel_editor(
        self,
        message: Message,
        player: Dict[str, Any]
    ) -> Dict[str, Union[str, Keyboard, None]]:
        if player['storyline_in_editor'] is None:
            player['storyline_in_editor'] = []
            return {
                "text": "Отправляйте сообщение для добавления слайдов."
            }

    def __show_settings(
        self,
        message: Message,
        player: Dict[str, Any]
    ) -> Dict[str, Union[str, Keyboard, None]]:
        return {
            "text": "Настройки.",
            "keyboard": keyboard_gen(
                [[{
                    "text": "Меню",
                    "color": "positive",
                    "payload": '"menu"'
                }]]
            )
        }

    def __generate_choice_keyboard(
        self,
        array: List[str],
        color: str = "secondary"
    ) -> Union[Keyboard, bool]:
        """
            Функция генерирует клавиатуру
            из массива выборов array.

            Если элементов 5 или меньше - отводит
            каждому по 1 строке.
            Если больше, отводит макс. 2 элемента
            на строку.
            Длинна массива не больше 10.

            :param array: массив с выбором
            :param color: цвет кнопок
            :return:  Keyboard
                      или False если len(array) > 10
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

    def __remove_player_game_flags(self, player: Dict[str, Any]) -> None:
        """
            Переводит флаги игрока player:
            game_is_choice,
            game_is_input_username
            в положение False.

            Используется чтобы при переходе
            в игру тебе показали сообщения
            с выбором и вводом имени заново.
        """
        player['game_is_choice'] = False
        player['game_is_input_username'] = False


proxy = Proxy(address="http://165.22.64.68:43377")
vk_bot = Bot(config.token)

bot_out = BotOutput()


@vk_bot.on.message()
async def on_message(message: Message) -> None:
    """
        Когда приходит новое сообщение,
        вызывает метод on_message класса BotOutput
        и отсылает пользователю что получил.
    """

    ans = bot_out.on_message(message)

    # Эффект печатанья сообщения.
    if ans.get('typing_delay'):
        await message.api.request(
            'messages.markAsRead',
            {'peer_id': message.from_id}
        )

        await message.api.request(
            'messages.setActivity',
            {
                'type': 'typing',
                'user_id': message.from_id
            }
        )
        sleep(ans['typing_delay'])

    await message(
        ans.get('text'),
        ans.get('attachment'),
        keyboard=ans.get('keyboard')
    )

if __name__ == '__main__':
    vk_bot.run_polling()
