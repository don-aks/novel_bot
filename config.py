example_storyline = [
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