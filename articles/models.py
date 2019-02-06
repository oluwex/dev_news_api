from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

from accounts.models import Profile

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


def make_slug(slug):
    result = Article.objects.filter(slug=slug)
    if result.exists():
        previous_id = result.last().id
        slug = "%s-%s" % (slug, previous_id)
        return make_slug(slug)
    return slug


@receiver(pre_save, sender=Article)
def slugify_title(sender, instance, *args, **kwargs):
    if not instance.slug:
        slugged = slugify(instance.title)
        instance.slug = make_slug(slugged)