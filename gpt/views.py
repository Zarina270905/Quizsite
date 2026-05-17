from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import ask_yandex_gpt

@login_required
def ask_question(request):
    result = None
    question = ""

    if request.method == 'POST':
        question = request.POST.get('question', '')
        if question:
            result = ask_yandex_gpt(question)

    context = {
        'title': 'Яндекс GPT',
        'result': result,
        'question': question,
        'hide_categories': True,
    }
    return render(request, 'gpt/test.html', context)

