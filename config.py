from dotenv import dotenv_values

token = dotenv_values()['TOKEN']

example_storyline = [
    {  # 0
        "text": "Вы проснулись на корабле.",
        "attachment": "photo-29559271_456242468,audio-2001694650_6694650"
    },
    {  # 1
        "text": "Никого на горизонте не виднелось.",
        "attachment": "audio212763299_456241453"
    },
    {  # 2
        "text": "Вдруг сзади вас кто-то бьет. Обернувшись, вас сковывает ужас... " +
        "Вы видите самого настоящего зомби. Ваши действия?",
        "attachment": "photo203817113_301033044",
        "choice": [
            "Ударить зомби",
            "Убежать",
            "Помолиться Аллаху"
        ]
    },
    {  # 3
        "if": {
            "choice": [2, 0]
        },
        "text": "Инстинкт подсказывает проверить этого зомби на прочность. И вы не прогадали. "+
        "Вы замахиваетесь и бьете прямо в челюсть. Голова зомби, словно пластилиновая падает на пол "+
        "а вместе с ней и все тело.",
        "attachment": "photo248015237_457245542"
    },
    {  # 4
        "if": {
            "choice": [2, 1]
        },
        "attachment": "photo248015237_457245263",
        "text": "Вы убежали и уперелись в борт корабля. Зомби подходит все ближе "
                + "и ближе...",
        "choice": [
            "Ударить зомби",
            "Прыгнуть в воду"
        ]
    },
    {  # 5
        "if": {
            "choice": [4, 0]
        },
        "text": "Когда вы замахнулись на зомби, чтобы ударить, он внезапно прошел мимо вас "
                + "и прыгнул в воду. \"Весьма странно...\" - подумали вы."
    },
    {  # 6
        "if": {
            "choice": ['or', [2, 0], [4, 0]]
        },
        "attachment": "photo248015237_457245493",
        "text": "\"Кажется, это последний\" - сказал ленивый автор этой Новеллы.\n"+
        "Хотя он не это сказал, но пофиг."
    },
    {  # 7
        "if": {
            "choice": ['or', [2, 0], [4, 0]]
        },
        "text": "Вдруг ваш мобильный зазвонил. Вы, оглядевшись по сторонам, достали телефон. "+
        "Номер телефона скрыт и не находится в ваших контактах. Кто же это может быть?..",
        "choice": ["Взять трубку", "Проигнорировать звонок"]
    },
    {  # 8
        "if": {
            "choice": [7, 0]
        },
        "text": 'Любопытство взяло верх и вы ответили на звонок. Вдруг там есть важная информация. "'+
        'Голос на той стороне трубки был мужским и брутальным. Он представился Борисом и спросил весьма '+
        'странный вопрос: "Вы человек?"',
        "choice": ["Да", "Нет", "Чево???"]
    },
    {  # 9
        "if": {
            "choice": [8, 0]
        },
        "attachment": "photo248015237_457245280",
        "text": 'Он невозмутимым голосом ответил "Манда" и положил трубку. Видимо какой-то розыгрыш...',
        "attachment": "photo248015237_457244565"
    },
    {  # 10
        "if": {
            "choice": [8, 1]
        },
        "attachment": "photo248015237_457245280",
        "text": 'Вам ответили "П*дора ответ" и положили трубку. Видимо какой-то розыгрыш...',
        "attachment": "photo248015237_457244565"
    },
    {  # 11
        "if": {
            "choice": [8, 2]
        },
        "attachment": "photo248015237_457245280",
        "text": 'Борис вам ответил "Таво" и положили трубку. Мда уж, голос явно не соответствует интеллекту...',
        "attachment": "photo248015237_457245503"
    },
    {  # 12
        "if": {
            "choice": [4, 0]
        },
        "text": "Вы решили проигнорировать странный звонок и искать решение проблемы."
    },
    {  # 13
        "if": {
            "choice": [4, 0]
        },
        "text": '"Что же делать... Что же делать..." - думаете вы. И я хз на самом деле.'
    },
    {  # 14
        "if": {
            "choice": [4, 0]
        },
        "text": 'Чо делать?',
        "choice": ["ХЗ", "Чото", "Чо???"]
    },
    {  # 15
        "if": {
            "choice": [14, 0]
        },
        "text": "Я тоже хз. Так шо пока!",
        "attachment": "photo248015237_457244540"
    },
    {  # 16
        "if": {
            "choice": [14, 1]
        },
        "text": "Да, чото надо делать. Но не сегодня. Пока!",
        "attachment": "photo248015237_457244658"
    },
    {  # 17
        "if": {
            "choice": [14, 2]
        },
        "text": "Через плеЧО, епта! Пока!"
    },
    {  # 18
        "if": {
            "choice": [5, 1]
        },
        "text": "Вы прыгнули в воду и вас тотчас съела голодная акула.",
        "attachment": "photo248015237_457244563"
    },
    {  # 19
        "if": {
            "choice": [5, 1]
        },
        "text": "Вы умерли.",
        "attachment": "photo248015237_457244445"
    },
    {  # 20
        "if": {
            "choice": [2, 2]
        },
        "text": "Вы решили помолиться Аллаху, но это не помогло. Вас съел голодный зомби.",
        "attachment": "photo248015237_457244448"
    },
    {  # 21
        "if": {
            "choice": [2, 2]
        },
        "text": "Вы умерли!",
        "attachment": "audio2000231970_456239688"
    },
    {  # 22
        "text": "Это все. НЕ ЗАБУДЬ АЦЕНИТЬ МАЮ НОВЕЛУ КЛАССОМ НЕ СУДИТИ СТРОГА!!!!))))) ПОКА!",
        "attachment": "photo248015237_457244626"
    }
]
