from rest_framework import serializers

from django.utils.html import strip_tags

from posts.models import Post

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80, allow_blank=False)

class PostSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='api_singlepost')
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    source = serializers.URLField()
    author = serializers.CharField(read_only=True)
    private = serializers.BooleanField()
    tag = serializers.CharField()

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data
    
class SinglePostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(format='%d %B %Y - %H:%M:%S')
    source = serializers.URLField()
    author = UserSerializer()
    private = serializers.BooleanField()
    tag = TagSerializer()
    likes = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data