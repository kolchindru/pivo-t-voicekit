import utils

free_answer_questions = [
    utils.Question(
        body="Какая сеть кофеен запустила в 1999 году экологическую программу Grounds for your Garden, в рамках которой отработанная кофейная гуща предоставляется желающим для компоста?",
        answers=[utils.AnswerOption(number=1, text="Старбакс", is_correct=True)],
        right_text="Крупнейшая кофейная сеть заботится об экологии!",
        wrong_text="Нет! Крупнейшая кофейная сеть Старбакс заботится об экологии!"
    ),
    utils.Question(
        body="Какая международная сеть кофеен приобрела успех на российском рынке лишь со второй попытки? Первый раз эта сеть открылась в 1996 году и проработала всего три года, а затем снова открылась уже 2010?",
        answers=[utils.AnswerOption(number=1, text="Dunkin Donuts", is_correct=True)],
        right_text="В точку!",
        wrong_text="Не-а! Это Dunkin Donuts."
    ),
]

multiple_choice_questions = [
    utils.Question(
        body="Спустя сколько лет после своего основания крупнейшая сеть кофеен Старбакс Кофе открыла первое кафе вне США?",
        answers=[utils.AnswerOption(number=1, text="25 лет", is_correct=True),
                 utils.AnswerOption(number=2, text="50 лет", is_correct=False),
                 utils.AnswerOption(number=3, text="6 лет", is_correct=False),
                 utils.AnswerOption(number=4, text="17 лет", is_correct=False)],
        right_text="Да, в 1996 открылась первая кофейня в Токио!",
        wrong_text="Нет! Компанию основали в 1971 году и только после убыточных 80-ых ей удалось открыть первую кофейню в Токио в 1996 году."
    ),
]

cases = [
    utils.Case(
        body="Правильно! Инвесторы заинтересовались твоей компанией, увидев, как ты разбираешься в области. Теперь ты можешь прокачать свою компанию:"
             "\nИнвесторы предлагают тебе:",
        outcomes=[utils.CaseAction(is_up=True, amount=10000000),
                  utils.CaseAction(is_up=True, amount=5000000)],
        choices=[utils.AnswerOption(number=1, text="10 000 000 рублей за долю 10% в твоей компании"),
                 utils.AnswerOption(number=2, text="5 000 000 рублей за долю 5% в твоей компании."),]
    ),
    utils.Case(
        body="Правильно! Инвесторы заинтересовались твоей компанией, увидев, как ты разбираешься в области. Теперь ты можешь прокачать свою компанию:"
             "\nИнвесторы предлагают тебе:",
        outcomes=[utils.CaseAction(is_up=True, amount=10000000),
                  utils.CaseAction(is_up=True, amount=5000000)],
        choices=[utils.AnswerOption(number=1, text="10 000 000 рублей за долю 10% в твоей компании"),
                 utils.AnswerOption(number=2, text="5 000 000 рублей за долю 5% в твоей компании."), ]
    ),
]
