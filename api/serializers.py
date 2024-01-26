from rest_framework import serializers

from django.utils.html import strip_tags

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    source = serializers.URLField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        data['content'] = data['content'].replace('&nbsp;', ' ')
        return data
    
class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=80, allow_blank=False)
