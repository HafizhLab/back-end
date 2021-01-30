import json
import pickle
import random
import sys

from django.http import HttpResponseBadRequest, JsonResponse

from hafizhlab.quran.models import Ayah, Juz, Surah

sys.path.append('machinelearning')

with open('machinelearning/lm_alquran.pickle', 'rb') as f:
    trained_model = pickle.load(f)

with open('machinelearning/tfidf_alquran.pickle', 'rb') as f:
    trained_model2 = pickle.load(f)

with open('machinelearning/ayahData.json') as f:
    ayah_korpus = json.load(f)['data']


def get_questions(request):
    mode = request.GET['mode']
    scope_type = request.GET['type']
    scope_id = request.GET['number']

    if scope_type.lower() == 'juz':
        scope = Juz.objects.get(id=scope_id)
    elif scope_type.lower() == 'surah':
        scope = Surah.objects.get(id=scope_id)
    else:
        return HttpResponseBadRequest(
            "type must either 'juz' or 'surah'"
        )

    ayah_count = scope.ayah_set.count()
    ayah = scope.ayah_set.all()[random.randrange(ayah_count)]

    if mode.lower() == 'word':
        key = 'questions'
        questions = []
        ayah_words = ayah.text.split()
        q_text = ayah_words[:3]
        q_remaining = ayah_words[3:]
        for word in q_remaining:
            options = [{
                'text': word,
                'isCorrect': True,
                'selected': False,
            }]
            for other in trained_model.next_word(q_text):
                options.append({
                    'text': other[1],
                    'isCorrect': False,
                    'selected': False,
                })
            questions.append({
                'text': ' '.join(q_text),
                'options': options,
            })
            q_text.append(q_remaining.pop(0))
        value = questions
    elif mode.lower() == 'verse':
        key = 'options'
        next_ayah = Ayah.objects.get(id=ayah.id+1)
        options = [{
            'text': next_ayah.text,
            'isCorrect': True,
            'selected': False,
        }]
        for other in trained_model2.get_top_n(next_ayah.text, ayah_korpus, n=3, print_top=False):
            options.append({
                'text': other[1]['text'],
                'isCorrect': False,
                'selected': False,
            })
        value = options
    else:
        return HttpResponseBadRequest(
            "mode must either 'verse' or 'word'"
        )

    random.shuffle(options)

    return JsonResponse({
        'text': ayah.text,
        key: value,
        'mode': mode,
        'title': ayah.surah.english_name,
        'number': ayah.number,
    })
