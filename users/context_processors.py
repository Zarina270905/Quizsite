from quizzes.views import menu

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Как это работает', 'url_name': 'how'},
    {'title': 'О сайте', 'url_name': 'about'},
]

def get_quizsite_context(request):
    return {'mainmenu': menu}