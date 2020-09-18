from deeppavlov import build_model, configs

model = build_model(configs.squad.squad, download=True)
# %%
docs = ['DeepPavlov is library for NLP and dialog systems.',
        'The name tf.train.AdamOptimizer is deprecated. Please use tf.compat.v1.train.AdamOptimizer instead.',
        'DeepPavlos is library',
        'What is Deep Learning?'
        ]
questions = ['What is DeepPavlov?']
for q in questions:
    print(q)
    for doc in docs:
        similarity = model([doc], [q])
        print('\t', similarity)
