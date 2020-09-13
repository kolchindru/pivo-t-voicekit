import utils

free_answer_questions = [
    utils.Question(
        body="Какая сеть кофеен запустила в 1999 году экологическую программу Grounds for your Garden, в рамках которой отработанная кофейная гуща предоставляется желающим для компоста?",
        answers=[utils.AnswerOption(number=1, text="Старбакс.", is_correct=True)],
        right_text="Крупнейшая кофейная сеть заботится об экологии!",
        wrong_text="Нет! Крупнейшая кофейная сеть Старбакс заботится об экологии!"
    ),
    utils.Question(
        body="Какая международная сеть кофеен приобрела успех на российском рынке лишь со второй попытки? Первый раз эта сеть открылась в 1996 году и проработала всего три года, а затем снова открылась уже 2010?",
        answers=[utils.AnswerOption(number=1, text="Данкин Донатс.", is_correct=True)],
        right_text="В точку!",
        wrong_text="Не-а! Это Данкин Донатс."
    ),
]

multiple_choice_questions = [
    utils.Question(
        body="Спустя сколько лет после своего основания крупнейшая сеть кофеен Старбакс Кофе открыла первое кафе вне Соединённых Штатов?",
        answers=[utils.AnswerOption(number=1, text="25 лет.", is_correct=True),
                 utils.AnswerOption(number=2, text="50 лет.", is_correct=False),
                 utils.AnswerOption(number=3, text="6 лет.", is_correct=False),
                 utils.AnswerOption(number=4, text="17 лет.", is_correct=False)],
        right_text="Да, в 1996 открылась первая кофейня в Токио!",
        wrong_text="Нет! Компанию основали в 1971 году и только после убыточных 80-ых ей удалось открыть первую кофейню в Токио в 1996 году."
    ),
]

cases = [
    utils.Case(
        body="Инвесторы заинтересовались твоей компанией, увидев, как ты разбираешься в области. Теперь ты можешь прокачать свою компанию:"
             "\nИнвесторы предлагают тебе:",
        outcomes=[utils.CaseAction(is_up=True, amount=10000000),
                  utils.CaseAction(is_up=True, amount=5000000)],
        choices=[utils.AnswerOption(number=1, text="10 000 000 рублей за долю 10% в твоей компании."),
                 utils.AnswerOption(number=2, text="5 000 000 рублей за долю 5% в твоей компании."), ]
    ),
    utils.Case(
        body="Конкуренты заинтересовались твоей компанией, увидев, как ты разбираешься в области. "
             "Они предлагают тебе 5 000 000 за то, чтобы ты закрыл свои офисы в городе Н. Что ты выберешь?",
        outcomes=[utils.CaseAction(is_up=True, amount=-5000000),
                  utils.CaseAction(is_up=True, amount=0)],
        choices=[utils.AnswerOption(number=1, text="Согласиться."),
                 utils.AnswerOption(number=2, text="Проигнорировать их."), ]
    ),
    utils.Case(
        body="В процессе хайринга вы находите крутого маркетолога. Он вроде как согласен принять ваш оффер, но "
             "только если вы в дополнение возьмете еще и его брата. С одной стороны, это хороший кандидат, "
             "который мог бы сильно помочь вам в продвижении ваших продуктов. С другой, это не очень разумный "
             "шаг — нанимать лишних сотрудников на ранних стадиях развития, да еще и по кумовским связям.",
        outcomes=[utils.CaseAction(is_up=True, amount=0),
                  utils.CaseAction(is_up=True, amount=0)],
        choices=[utils.AnswerOption(number=1, text="Взять обоих братьев на работу. На свой страх и риск."),
                 utils.AnswerOption(number=2, text="Отказаться от них."), ]
    ),
]

companies = utils.Domains(
    body="Привет! В ОЛего тебе нужно построить собственную компанию с нуля. Меня часто спрашивают: 'С чего ты начинал?' С воли к жизни. Жить я хотел, а не прозябать. Давай создадим твою компанию. Чем она будет заниматься? [предложено на основе твоих предпочтений]:\n",
    choices=[utils.AnswerOption(number=1, text="Эко-френдли кофейня.", id="coffee"),
             utils.AnswerOption(number=2, text="Маникюрный салон.", id="nails"),
             utils.AnswerOption(number=3, text="Сервис по аренде самокатов.", id="scooter")],
)
