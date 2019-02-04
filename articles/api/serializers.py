from rest_framework.serializers import (
    EmailField,
    CharField,
    StringRelatedField,
    HyperlinkedIdentityField,
    ModelSerializer,
    HyperlinkedModelSerializer,
    ValidationError
)

from ..models import Article


class ArticleSerializer(ModelSerializer):
# class ArticleSerializer(HyperlinkedModelSerializer):

    author = StringRelatedField()
    url = HyperlinkedIdentityField(
        view_name='articles-api:retrieve_article',
        lookup_field='slug'
    )
    edit_url = HyperlinkedIdentityField(
        view_name='articles-api:update_article',
        lookup_field='slug'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='articles-api:delete_article',
        lookup_field='slug'
    )

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
            'content',
            'author',
            'timestamp',
            'edit_url',
            'delete_url',
        ]


class ArticleCreateSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
        ]