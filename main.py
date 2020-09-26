from time import sleep

import config


class Novel:
    """
        Класс, содержащий новеллу с одним игроком
    """

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
        self.slide_id = 2

    def move(self, choice_id: int = None) -> dict or False:
        """
            Вернуть информацию об одном слайде начиная с self.slide_id
            :param choice_id: (int) id выбора на слайде self.slide_id
            :return: slide (dict) or False if this slide is last
        """
        # пока условия в слайде будут выполнены (если они есть)
        while True:
            # Если слайда не существует
            if self.slide_id >= len(self.storyline):
                return False

            slide = self.storyline[self.slide_id]
            # Есть ли условие в слайде
            if 'if' in slide:
                if self._is_condition(slide['if']):
                    break
                else:
                    self.slide_id += 1
            else:
                break

        # Если есть выбор и choice_id
        if 'choice' in slide and choice_id is not None:
            self.player_choices[self.slide_id] = choice_id
            self.slide_id += 1
            # Возвращаем следующий слайд после выбора
            # Нужно вызвать еще раз для проверки условий
            return self.move()
        else:
            self.slide_id += 1

        return slide

    def play_in_console(self, sleep_time: int = 0):
        """
            Играть в консоле.
            :param sleep_time: (int) delay show slides in seconds
        """
        print(f'Вы начали играть в новеллу "{self.name}"')
        if self.is_input_username:
            self.username = input("Введите свое имя: ")

        move = self.move()
        while move:
            print(move['text'])  # выводим текст
            if 'choice' in move:  # Если есть выбор
                # Функция для ввода выбора
                while True:
                    for i, option in enumerate(move[2]):
                        print(f'{i + 1}. {option}')

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
                move = self.move(choice)
                continue

            move = self.move()  # вписываем предыдущий id слайда
            sleep(sleep_time)

        print("Новелла закончилась")

    def _is_condition(self, conditions: dict) -> bool:
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
