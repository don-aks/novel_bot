from vkbottle import Bot, Message, Proxy
from vkbottle.keyboard import Keyboard, keyboard_gen

from main import Novel
import config


class BotOutput:
    players = {}

    def generate_keyboard(self,
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

    def get_player_info(self, vk_id: int) -> dict:
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
                "is_choice": False
            }
            return player


proxy = Proxy(address="http://212.87.220.2:3128")
bot = Bot(config.token)

bot_output = BotOutput()
k_next_slide = keyboard_gen(
    [
        [
            {'text': "Дальше ➡", "color": "primary"}
        ]
    ]
)


@bot.on.message()
async def on_message(message: Message) -> str or None:
    """
        Реагирует на новые сообщения в ВК.
        :param message: object Message
        :returns: str answer or None
    """
    print("on_message")
    print(message.payload)

    player = bot_output.get_player_info(message.from_id)
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
                return "Введите число или используйте клавиатуру!"
            else:
                len_choice = len(novel.storyline[novel.slide_id]['choice'])
                if not len_choice >= choice > 0:
                    return (f"Введите число от 1 до {len_choice}"+
                            "или используйте клавиатуру!")

            choice -= 1

        move = novel.move(choice)
        player['is_choice'] = False
    else:
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
            await message(
                answer, attachment,
                keyboard=bot_output.generate_keyboard(move['choice'])
            )
        else:
            # Возвращаем текст и аттачи
            await message(move['text'], attachment, keyboard=k_next_slide)
    else:
        await message("Новелла закончена.", keyboard=keyboard_gen([]))


if __name__ == '__main__':
    bot.run_polling()
