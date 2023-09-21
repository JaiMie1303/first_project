from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление данных из определенной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все посты {options["category"]} категории? y/n:')

        if answer != 'y':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            cat = Category.objects.get(category=options['category'])
            posts = Post.objects.filter(post_category=cat)
            # posts.delete()
            self.stdout.write(self.style.SUCCESS(f"Все посты категории{options['category']} удалены "))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Не удалось найти категорию {options['category']}"))