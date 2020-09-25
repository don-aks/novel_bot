from vkbottle import Bot, Message, Proxy
from vkbottle.framework.bot.templates.echo import Echo

from main import Novel
import config

class VKBot:
    """
        Методы класса возвращают
        строку или клавиатуру 
        с ответом для пользователя.
    """

    def move(self):
        pass

proxy = Proxy(address="http://157.230.103.189:37826")
bot = Bot(config.token)

novel = Novel("test", config.example_storyline, False, False)
slide_id = 0
vk_bot = VKBot()

is_choice = False

@bot.on.message()
async def on_message(ans: Message):
    """
        Обработчик сообщений
    """
    global slide_id, is_choice
    print(f'1. {slide_id}')

    move = novel.move(slide_id)
    if move:
        if move[2]: # Если есть выбор
            # Если выбор был озвучен
            if is_choice:
                # Проверять, является ли введенное сообщение выбором
                try:
                    choice = int(ans.text)
                except ValueError:
                    return "Введенное значение должно быть числом!"
                else:
                    if not len(move[2]) >= choice > 0:
                        return f"Введите цифру от 1 до {len(move[2])}!"
                choice -= 1
                move = novel.move(move[0], choice)
                is_choice = False
            else:
                answer = move[1]+'\n'
                for i, option in enumerate(move[2]):
                    answer += f'{i+1}. {option}\n'
                answer += "Введите номер выбора."

                await ans(answer)
                is_choice = True
        else:
            await ans(move[1])

        slide_id = move[0]
    else:
        slide_id = 0
        return "Новелла закончена"
    print(f'2. {slide_id}')


if __name__ == '__main__':
    bot.run_polling()