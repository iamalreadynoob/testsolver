import json
import google.generativeai as gemini


def starter():
    with open('config.json', 'r') as f:
        config = json.load(f)

    gemini.configure(api_key=config['api_key'])
    model = gemini.GenerativeModel(model_name=config['model_name'])
    session = model.start_chat(history=[])

    return session, gemini


def answer(question, options, model):
    with open('config.json', 'r') as f:
        config = json.load(f)

    times = config['ask_times']

    counter = {}

    for i in range(len(options)):
        counter[i] = 0

    prompt = "give me the only the letter of the correct option for this question, no explaination:\n{}".format(question)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    letters = letters[:len(options)]

    for i in range(len(options)):
        prompt += '\n{}) {}'.format(letters[i], options[i])

    for i in range(times):
        response = model.send_message(prompt).text.lower().replace(')', '')

        if len(response) > 1:
            words = response.split(' ')

            for word in words:
                if len(word) == 1 and word in letters:
                    response = word
                    break

            if len(response) > 1:
                for j in range(len(response)):
                    if response[j] in letters:
                        response = response[j]
                        break

        counter[letters.index(response)] += 1

    most_vote = max(counter.values())

    for key in counter.keys():
        if counter[key] == most_vote:
            return options[key]