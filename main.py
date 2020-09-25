from time import sleep

import config

class Novel():

    def __init__(self, name: str, storyline: list,
                is_hentai: bool, is_input_username: bool):
        """
            :param name: Имя новеллы
            :param storyline: Список слайдов для показа
            :param is_hentai: Присутствует ли контент для взрослых
            :param is_input_username: Давать ли возможность пользователю ...
                ... ввести свое имя
        """
        self.name = name
        self.storyline = storyline
        self.is_hentai = is_hentai
        self.is_input_username = is_input_username
        self.username = None if is_input_username else False

        self.player_choices = {}

    def play_in_console(self, sleep_time=0):
        """
            Играть в консоле.
            :param sleep_time: (int) delay shows slides in seconds
        """
        print(f'Вы начали играть в новеллу "{self.name}"')
        if self.is_input_username:
            self.username = input("Введите свое имя: ")

        move = self.move()
        while move:
            print(move[1]) # выводим текст
            if move[2]: # Если есть выбор
                # Функция для ввода выбора
                while True:
                    for i, option in enumerate(move[2]):
                        print(f'{i+1}. {option}')

                    inp = input("Введите номер выбора: ")
                    try:
                        choice = int(inp)
                    except ValueError:
                        print("Введенное значение должно быть числом!")
                    else:
                        if not len(move[2]) >= choice > 0:
                            print(f"Введите цифру от 1 до {len(move[2])}!")
                        else:
                            break
                choice -= 1

                # Отсылаем move свой выбор
                move = self.move(move[0], choice)
                continue

            move = self.move(move[0]) # вписываем предыдущий id слайда
            sleep(sleep_time)

        print("Новелла закончилась")

    def move(self, slide_id=0, choice_id=None):
        """
            Вернуть информацию об одном слайде начиная со slide_id.
            :param slide_id: (int)
            :param choice_id: (int) id выбора на слайде slide_id
            :return: (next slide_id, slide text, slide choice or None)
                     or False if this slide is last
        """
        while True: # пока условия в слайде будут выполнены (если они есть)
            try:
                slide = self.storyline[slide_id]
            except IndexError:
                return False

            # Есть ли условие в слайде
            if 'if' in slide:
                if self._is_condition(slide['if']):
                    slide = slide['slide']
                    break
                else:
                    slide_id += 1
            else:
                break


        if 'choice' in slide:
            # если не указан id выбора, возвращать массив с выбором
            if choice_id == None:
                return slide_id, slide['text'], slide['choice']
            # если указан, записываем
            self.player_choices[slide_id] = choice_id

        slide_id += 1
        return slide_id, slide['text'], None

    def _is_condition(self, conditions: dict):
        """
            Проверка условий conditions
            :param conditions: dict conditions in slide
            :return: bool
        """
        for key, value in conditions.items():
            if key == "choice":
                if not isinstance(value[1], list):
                    value = [value]
                for arr in value:
                    if self.player_choices.get(arr[0]) != arr[1]:
                        return False

        return True


if __name__ == '__main__':
    novel = Novel("test", config.example_storyline, False, False)
    novel.play_in_console()