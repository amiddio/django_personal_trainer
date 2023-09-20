from django.shortcuts import render


def page_handler404(request, exception):
    """Обработка ошибки 404"""

    return render(request=request, template_name='errors/page_error.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница не существует',
    })


def page_handler500(request):
    """Обработка ошибки 500"""

    return render(request=request, template_name='errors/page_error.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта',
    })

