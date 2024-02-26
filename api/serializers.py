import re

from rest_framework import serializers
from rest_framework.reverse import reverse as rest_reverse

from django.utils.html import strip_tags

from posts.models import Post
from tags.models import Tag

class ConditionalHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):

    def to_representation(self, value):
        context = self.context.get('request')
        if context and context.resolver_match.view_name == 'api_singletag':
            return  value.id
        return super().to_representation(value)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

class TagSerializer(serializers.ModelSerializer):
    id = ConditionalHyperlinkedIdentityField(view_name='api_singletag')
    name = serializers.CharField(max_length=80, allow_blank=False)
    created_at = serializers.DateField(read_only=True, format='%d %B %Y')

    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='api_singlepost')
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    source = serializers.URLField()
    author = serializers.CharField(read_only=True)
    tag = serializers.CharField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'source', 'author', 'tag']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data

class SinglePostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(format='%d %B %Y - %H:%M:%S', read_only=True)
    source = serializers.URLField()
    author = UserSerializer(read_only=True)
    tag = TagSerializer()
    likes = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data