from config import ROOT_DIR
from helpbot.config import ConfigBot
from helpbot.conversation import AnswerHandler


config = ConfigBot.load(ROOT_DIR, 'helpbot/config.yaml')
answer_handler = AnswerHandler(config)


def get_answer(query):
    return answer_handler.predict_text_classes(query)


if __name__ == '__main__':
    print(get_answer('gantt chart'))
