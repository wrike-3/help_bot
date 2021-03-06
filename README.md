# telegram_help_bot
[![Build Status](https://travis-ci.org/wrike-3/help_bot.svg?branch=master)](https://travis-ci.org/wrike-3/help_bot)
## About
Telegram bot for a help center
- `chatbot.py` - telegram bot for messaging
- `support_model.py` - question answering AI
- `models` - answering models
- - `elasticsearch_baseline` - fuzzy search
- - `bert_emb_baseline` - BERT embedding ranking model
- - `bpe_baseline` - BPE embedding ranking model
- - `tfidf` - TFIDF classification model
- Run bot `python chatbot.py`
- Available in telegram by address `@wrike_help_bot`
## Features
- answer question
- estimate question
- add new question with answer
- show history

## Finite automaton
![](https://github.com/wrike-3/help_bot/blob/master/chatbot_graph.png)



