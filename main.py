from time import sleep

def input_int(text, error="Введите число!"):
	while True:
		inp = input(text)
		try:
			return int(inp)
		except ValueError:
			print(error)

class Novel():

	def __init__(self, name: str, storyline: list, hentai: bool, id_author: int, show_author: bool,
	input_username: bool):
		self.name = name
		self.storyline = storyline
		self.hentai = hentai
		self.id_author = id_author
		self.show_author = show_author
		self.input_username = input_username
		self.username = None if input_username else False

		self.player_choices = []

	def play(self):
		print(f'Вы начали играть в новеллу "{self.name}"')
		if self.show_author:
			print(f"@id{self.id_author} (Автор)")
		if self.input_username:
			self.username = input("Введите свое имя: ")
		self._iters_storyline(self.storyline, [])
		print("Новелла закончилась")

	def move(self, position: list):
		pos = self.storyline
		for i in position:
			try:
				pos = pos[i]['storyline']
			except KeyError:
				pos = pos[i]
		


	def _iters_storyline(self, storyline: list, branches: list):
		for slide_id, slide in enumerate(storyline):
			if 'if' in slide:
				if self._is_condition(slide['if']):
					self._iters_storyline(slide['storyline'], branches+[slide_id])
					continue
				else:
					continue

			print(slide['text'])
			sleep(0)
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

				self.player_choices.append([branches+[slide_id], choice])

	def _is_condition(self, conditions: dict):
		for key, value in conditions.items():
			if key == "choice":
				if not isinstance(value[1], list):
					value = [value]
				for arr in value:
					if not isinstance(arr[0], list):
						arr[0] = [arr[0]]
					if arr not in self.player_choices:
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
			"storyline": [
				{
					"text": "После удара, голова зомби отлетела и упала на пол. Зомби повержен."
				},
				{
					"text": "Вы пережили зомби апокалипсис!"
				}
			]
		},
		{
			"if": {
				"choice": [2, 1]
			},
			"storyline": [
				{
					"text": "Вы убежали и уперелись в борт корабля. Зомби подходит все ближе"+
					"и ближе. Ваши действия?",
					"choice": [
						"Ударить зомби",
						"Прыгнуть в воду"
					]
				},
				{
					"if": {
						"choice": [[4, 0], 0]
					},
					"storyline": [
						{
							"text": "Когда вы замахнулись на зомби, он понял с кем связался, и прыгнул"+
							"в воду."
						},
						{
							"text": "Вам позвонили. Имя неизвестно. Брать трубку?",
							"choice": ["Да", "Нет"]
						},
						{
							"if": {
								"choice": [[4, 1, 1], 0],
							},
							"storyline": [
								{
									"text": 'У вас спросили: "Вы человек?" Что ответить?',
									"choice": ["Да", "Нет", "Чево???"]
								},
								{
									"if": {
										"choice": [[4, 1, 2, 0], 0]
									},
									"storyline": [
										{
											"text": 'Вам ответили "Манда" и положили трубку.'
										}
									]
								},
								{
									"if": {
										"choice": [[4, 1, 2, 0], 1]
									},
									"storyline": [
										{
											"text": 'Вам ответили "П*дора ответ" и положили трубку.'
										}
									]
								},
								{
									"if": {
										"choice": [[4, 1, 2, 0], 2]
									},
									"storyline": [
										{
											"text": 'Вам ответили "Таво" и положили трубку.'
										}
									]
								}
							]
						},
						{
							"text": "Вы решили проигнорировать странный звонок и искать решение проблемы."
						},
						{
							"text": '"Что же делать... Что же делать..." - думаете вы. И я хз на самом деле.'
						},
						{
							"text": 'Чо делать?',
							"choice": ["ХЗ", "Чото", "Чо???"]
						},
						{
							"if": {
								"choice": [[4, 1, 5], 0]
							},
							"storyline": [
								{
									"text": "Я тоже хз. Так шо пока!"
								}
							]
						},
						{
							"if": {
								"choice": [[4, 1, 5], 1]
							},
							"storyline": [
								{
									"text": "Да, чото надо делать. Но не сегодня. Пока!"
								}
							]
						},
						{
							"if": {
								"choice": [[4, 1, 5], 2]
							},
							"storyline": [
								{
									"text": "Через плеЧО, епта! Пока!"
								}
							]
						}
					]
				},
				{
					"if": {
						"choice": [[4, 0], 1]
					},
					"storyline": [
						{
							"text": "Вы прыгнули в воду и вас тотчас съела голодная акула"
						},
						{
							"text": "Вы умерли!"
						}
					]
				}
			]
		},
		{
			"if": {
				"choice": [2, 2]
			},
			"storyline": [
				{
					"text": "Вы решили помолиться Аллаху, но это не помогло. Вас съел голодный зомби."
				},
				{
					"text": "Вы умерли!"
				}
			]
		},
		{
			"text": "Это все. НЕ ЗАБУДЬ АЦЕНИТЬ МАЮ НОВЕЛУ ЛАЙКОМ НЕ СУДИТИ СТРОГА!!!!))))) ПОКА!"
		}
	]

	novel = Novel("test", storyline, False, 0, True, False)
	novel.play()