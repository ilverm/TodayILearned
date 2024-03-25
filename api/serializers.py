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
    slug = serializers.SlugField()
    content = serializers.CharField()
    source = serializers.URLField()
    author = serializers.CharField(read_only=True)
    tag = serializers.CharField(allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'source', 'author', 'tag']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data

class SinglePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    slug = serializers.SlugField()
    content = serializers.CharField()
    created_at = serializers.DateField(format='%d %B %Y - %H:%M:%S', read_only=True)
    source = serializers.URLField()
    author = UserSerializer(read_only=True)
    tag = TagSerializer()
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'created_at', 'source', 'author', 'tag', 'likes']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.source = validated_data.get('source', instance.source)

        # new tag
        validated_tag = validated_data.get('tag', instance.tag)['name']
        tag, created = Tag.objects.get_or_create(name=validated_tag)
        if not created:
            tag.name = validated_tag
        tag.save()
        instance.tag = tag
        instance.save()
        return instance