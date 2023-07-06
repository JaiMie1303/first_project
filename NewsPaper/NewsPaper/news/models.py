from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(
            posts_rating_sum=Sum('post_rating') * 3
        )

        author_comments_rating = Comment.objects.all().filter(user_id=self.user).aggregate(
            comments_rating_sum=Sum('comment_rating')
        )

        print(author_posts_rating)
        print(author_comments_rating)

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum']
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=128, unique=True)


class Post(models.Model):

    NEWS = 'NW'
    ARTICLE = 'AR'

    TYPES = [(NEWS, 'Новость'), (ARTICLE, 'Статья')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_of_post = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category)
    type_post = models.CharField(max_length=2, choices=TYPES)
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        return self.post_text[:125] + '...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_PostCategory = models.ManyToManyField(Category)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length=255)
    date_of_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
