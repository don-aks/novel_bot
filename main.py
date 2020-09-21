from time import sleep

def input_int(text, error="Введите число!"):
    while True:
        inp = input(text)
        try:
            return int(inp)
        except ValueError:
            print(error)

class Novel():

    def __init__(self, name: str, storyline: list, exists_hentai: bool, 
                id_author: int, show_author: bool, is_input_username: bool):
        self.name = name
        self.storyline = storyline
        self.exists_hentai = exists_hentai
        self.id_author = id_author
        self.show_author = show_author
        self.is_input_username = is_input_username
        self.username = None if is_input_username else False

        self.player_choices = {}

    def play(self, sleep_time=0):
        """Играть в однопоточном режиме."""
        print(f'Вы начали играть в новеллу "{self.name}"')
        if self.show_author:
            print(f"@id{self.id_author} (Автор)")
        if self.is_input_username:
            self.username = input("Введите свое имя: ")

        move = self.move()
        while move:
            move = self.move(move) # вписываем предыдущее значение
            sleep(sleep_time)

        print("Новелла закончилась")

    def move(self, slide_id=0):
        """
            Показать один слайд начиная с slide_id.
            Возвращает slide_id (int) после этого слайда или False, если слайдов
            доступных для показа больше нет.
        """
        while True: # пока условия (если есть) в слайде будут выполнены
            try:
                slide = self.storyline[slide_id]
            except IndexError:
                return False

            if 'if' in slide:
                if self._is_condition(slide['if']):
                    slide = slide['slide']
                    break
                else:
                    slide_id += 1
            else:
                break

        print(slide['text'])

        if 'choice' in slide:
            for i, option in enumerate(slide['choice']):
                print(f'{i+1}. {option}')

            # Input choice
            while True:
                choice = input_int("Введите цифру выбора: ")
                if not len(slide['choice']) >= choice > 0:
                    print(f"Введите цифру от 1 до {len(slide['choice'])}!")
                    continue
                break
            choice -= 1

            self.player_choices[slide_id] = choice

        slide_id += 1
        return slide_id

    def _is_condition(self, conditions: dict):
        for key, value in conditions.items():
            if key == "choice":
                if not isinstance(value[1], list):
                    value = [value]
                for arr in value:
                    if self.player_choices.get(arr[0]) != arr[1]:
                        return False

        return True


if __name__ == '__main__':
    storyline = [
        {
            "text": "Вы проснулись на корабле.",
            "photo": "photo_id_in_vk",
            "audio": "audio_id_in_vk"
        },
        {
            "text": "Никого на горизонте не виднелось."
        },
        {
            "text": "Вдруг вас бьет кто-то сзади. Обернувшись, вы обнаруживаете, что это самый настоящий"+
            "зомби!!! Ваши действия?",
            "choice": [
                "Ударить зомби",
                "Убежать",
                "Помолиться Аллаху"
            ]
        },
        {
            "if": {
                "choice": [2, 0]
            },
            "slide": {
                "text": "После удара, голова зомби отлетела и упала на пол. Зомби повержен."
            }
        },
        {
            "if": {
                "choice": [2, 0]
            },
            "slide": {
                "text": "Вы пережили зомби апокалипсис!"
            }
        },
        {
            "if": {
                "choice": [2, 1]
            },
            "slide": {
                "text": "Вы убежали и уперелись в борт корабля. Зомби подходит все ближе"+
                "и ближе. Ваши действия?",
                "choice": [
                    "Ударить зомби",
                    "Прыгнуть в воду"
                ]
            }
        },
        {
            "if": {
                "choice": [5, 0]
            }, 
            "slide": {
                "text": "Когда вы замахнулись на зомби, он понял с кем связался, и прыгнул"+
                "в воду."
            }
        },
        {
            "if": {
                "choice": [5, 0]
            },
            "slide": {
                "text": "Вам позвонили. Имя неизвестно. Брать трубку?",
                "choice": ["Да", "Нет"]
            }
        },        
        {
            "if": {
                "choice": [7, 0]
            }, 
            "slide": {
                "text": 'У вас спросили: "Вы человек?" Что ответить?',
                "choice": ["Да", "Нет", "Чево???"]
            },
        },
        {
            "if": {
                "choice": [8, 0]
            }, 
            "slide": {
                "text": 'Вам ответили "Манда" и положили трубку.'
            }
        },
        {
            "if": {
                "choice": [8, 1]
            }, 
            "slide": {
                "text": 'Вам ответили "П*дора ответ" и положили трубку.'
            }
        },
        {
            "if": {
                "choice": [8, 2]
            },
            "slide": {
                "text": 'Вам ответили "Таво" и положили трубку.'
            }
        },
        {
            "if": {
                "choice": [5, 0]
            }, 
            "slide": {
                "text": "Вы решили проигнорировать странный звонок и искать решение проблемы."
            }
        },
        {
            "if": {
                "choice": [5, 0]
            },
            "slide": {
                "text": '"Что же делать... Что же делать..." - думаете вы. И я хз на самом деле.'
            }
        },
        {
            "if": {
                "choice": [5, 0]
            },
            "slide": {
                "text": 'Чо делать?',
                "choice": ["ХЗ", "Чото", "Чо???"]
            }
        },
        {
            "if": {
                "choice": [14, 0]
            },
            "slide": {
                "text": "Я тоже хз. Так шо пока!"
            }
        },
        {
            "if": {
                "choice": [14, 1]
            },
            "slide": {
                "text": "Да, чото надо делать. Но не сегодня. Пока!"
            }
        },
        {
            "if": {
                "choice": [14, 2]
            },
            "slide": {
                "text": "Через плеЧО, епта! Пока!"
            }
        },
        {
            "if": {
                "choice": [5, 1]
            },
            "slide": {
                "text": "Вы прыгнули в воду и вас тотчас съела голодная акула"
            }
        },
        {
            "if": {
                "choice": [5, 1]
            },
            "slide": {
                "text": "Вы умерли"
            }
        },
        {
            "if": {
                "choice": [2, 2]
            },
            "slide": {
                "text": "Вы решили помолиться Аллаху, но это не помогло. Вас съел голодный зомби."
            }
        },
        {
            "if": {
                "choice": [2, 2]
            },
            "slide": {
                "text": "Вы умерли!"
            }
        },
        {
            "text": "Это все. НЕ ЗАБУДЬ АЦЕНИТЬ МАЮ НОВЕЛУ ЛАЙКОМ НЕ СУДИТИ СТРОГА!!!!))))) ПОКА!"
        }
    ]

    novel = Novel("test", storyline, False, 0, True, False)
    novel.play()