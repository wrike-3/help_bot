# %%
import re

dialogs = ['''
(04:23:01 PM) ХХХ: Hi
(04:23:06 PM) * YYY joined the chat *
(04:23:19 PM) XXX: Hi ХХХ!
(04:23:29 PM) YYY: Just 1 more question; How can I see my tasks (created in Wrike) in my Outlook Calendar?
(04:24:56 PM) XXX: You can create a iCal link for that. Here you can find the instructions: https://help.wrike.com/hc/en-us/articles/210324085-iCalendar-Feeds
(04:34:23 PM) YYY: OK. Thanks. That works fine.
(04:34:40 PM) X: Glad to hear that!
''',
           '''
           Chat started: 2019-01-02 08:59 PM UTC
           
           (08:59:24 PM) XXX: critical path function?
           (08:59:31 PM) * YYY joined the chat *
           (08:59:39 PM) YYY: Hi XXX!
           (08:59:51 PM) YYY: One moment, please. I'll find the relevant info for you
           (09:00:00 PM) XXX: hi
           (09:01:16 PM) YYY: Here you go - https://help.wrike.com/hc/en-us/articles/209604189-Critical-Path . This article described the functionality you're looking for, however, it's available starting with a Business level subscription and based on my info you're currently signed up to a Professional-level trial, so this one will not be available for you at the moment
           ''',
           '''
           Chat started: 2019-01-02 20:59 AM UTC
           
           (08:59:24 AM) XXX: critical path function?
           (08:59:31 AM) * YYY joined the chat *
           (08:59:39 AM) YYY: Hi XXX!
           (08:59:51 AM) YYY: One moment, please. I'll find the relevant info for you
           (09:00:00 AM) XXX: hi
           (09:01:16 AM) YYY: Here you go - https://help.wrike.com/hc/en-us/articles/209604189-Critical-Path . This article described the functionality you're looking for, however, it's available starting with a Business level subscription and based on my info you're currently signed up to a Professional-level trial, so this one will not be available for you at the moment
           '''
           ]


# %%


def get_names(d):
    names = re.findall('\n\(\d+:\d+:\d+ [P|A]M\) (.*?): .*', d)
    return names


def parse_dialog(d):
    questions = re.findall(': (.*\?)', d)
    answers = re.findall('(https?:.*?)\s.*', d)
    return questions, answers


for d in dialogs:
    print(d)
    names = get_names(d)
    print('names:', names)
    questions, answers = parse_dialog(d)
    print('questions: ', questions)
    print('answers:', answers)
    print()

