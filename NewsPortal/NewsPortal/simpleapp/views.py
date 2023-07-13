from django.views.generic import ListView, DetailView
from .models import NewsPortal


class NewsList(ListView):
    model = NewsPortal
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    queryset = NewsPortal.objects.order_by('-time_pub')


class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = NewsPortal
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'
