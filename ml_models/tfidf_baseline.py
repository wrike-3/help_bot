from config import ROOT_DIR
from helpbot.config import ConfigBot
from helpbot.conversation import AnswerHandler


config = ConfigBot.load(ROOT_DIR, 'helpbot/config.yaml')
answer_handler = AnswerHandler(config)


def get_answer(query):
    answer = answer_handler.return_answer(query)
    return answer


if __name__ == '__main__':
    print(get_answer('gantt chart'))

