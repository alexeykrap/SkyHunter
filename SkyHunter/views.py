from django.shortcuts import render


# Create your views here.
def main(request):
    if request.user.id:
        # логика
        if request.method == 'GET':
            # отправляем пользователю главную страницу
            # context['verify_orders'] = new_verify_orders
            return render(request, 'main.html')
        if request.method == 'POST':
            # что-то делаем с запросом
            pass
    else:
        # перенаправление на страницу регистрации
        # context['verify_orders'] = new_verify_orders
        return render(request, 'main.html')