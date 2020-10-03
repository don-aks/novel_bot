from time import sleep

import config


class Novel:
    """
        Класс, содержащий новеллу
        для одного игрока.
    """

    def __init__(self,
                 storyline: list,
                 slide_id: int = 0,
                 is_input_username: bool = False,
                 username: str = None):
        """
            :param storyline: Список слайдов для показа.
            :param slide_id: id слайда с которого
                             начинать показ.
            :param is_input_username: Нужно ли
                                      имя пользователя.
            :param username: Имя пользователя.
                             По умолчанию None.
        """
        self.storyline = storyline
        self.is_input_username = is_input_username
        self.username = username

        self.player_choices = {}
        self.slide_id = slide_id
        self.vars = {}

    def step(self, choice_id: int = None) -> dict or False:
        """
            Вернуть информацию об одном слайде
            начиная с self.slide_id

            :param choice_id: (int) id выбора на слайде
                              self.slide_id
            :return: slide (dict)
                     or False if this slide is last
        """
        # пока условия в слайде будут выполнены
        # (если они есть)

        if (self.slide_id == 0 and self.is_input_username
           and not (isinstance(self.username, str) or self.username)):
            raise NameError("self.username is empty.")

        while True:
            # Если слайда не существует
            if self.slide_id >= len(self.storyline):
                return False

            slide = self.storyline[self.slide_id]
            # Есть ли условие в слайде
            if 'if' in slide:
                if self.__is_condition(slide['if']):
                    break
                else:
                    self.slide_id += 1
            else:
                break

        # Если есть выбор и choice_id
        if 'choice' in slide and choice_id is not None:
            self.player_choices[self.slide_id] = choice_id
            self.slide_id += 1
            # Возвращаем следующий слайд после
            # выбора

            # Нужно вызвать еще раз для проверки
            # условий внутри нового слайда
            return self.step()
        elif 'choice' not in slide:
            self.slide_id += 1

        return slide

    def play_in_console(self, sleep_time: int = 0):
        """
            Играть в консоле.
            :param sleep_time: (int) delay show slides in seconds
        """
        if self.is_input_username:
            self.username = input("Введите свое имя: ")

        step = self.step()
        while step:
            sleep(sleep_time)
            # Выводим текст
            print(step['text'])

            # Если есть выбор
            if 'choice' in step:
                # Функция для ввода выбора
                while True:
                    for i, option in enumerate(step['choice']):
                        print(f'{i + 1}. {option}')

                    inp = input("Введите номер выбора: ")
                    try:
                        choice = int(inp)
                    except ValueError:
                        print("Введенное значение должно быть числом!")
                    else:
                        len_choice = len(step['choice'])
                        if not len_choice >= choice > 0:
                            print(f"Введите цифру от 1 до {len_choice}!")
                        else:
                            break
                choice -= 1

                # Отсылаем свой выбор
                step = self.step(choice)
                continue

            # вписываем предыдущий id слайда
            step = self.step()

        print("Новелла закончилась")

    def __is_condition(self, conditions: dict) -> bool:
        """
            Проверка условий conditions
            :param conditions: dict conditions in slide
            :return: bool
        """
        for key, value in conditions.items():
            if key == "choice":
                operator = 'and'
                # Если несколько выборов
                if isinstance(value[1], list):
                    operator = value.pop(0)
                else:
                    value = [value]
                for arr in value:
                    if (operator == 'and' and
                       self.player_choices.get(arr[0]) != arr[1]):
                        return False
                    elif operator == 'or':
                        if self.player_choices.get(arr[0]) == arr[1]:
                            break  # True
                        elif arr == value[-1]:
                            return False
                    print()
            elif key == "username":
                if self.username != value:
                    return False
            # Пользовательские переменные
            else:
                if self.vars.get(key) != value:
                    return False

        return True


if __name__ == '__main__':
    novel = Novel(config.example_storyline, is_input_username=True)
    novel.play_in_console()
