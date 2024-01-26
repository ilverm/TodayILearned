from posts.models import Post
from tags.models import Tag

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse as rest_reverse

from .serializers import PostSerializer, TagSerializer

class ApiHome(APIView):
    """
    This endpoint provides the link for the "post" endpoint
    """
    def get(self, request):
        data = {
            'Posts': rest_reverse('api_posts', request=request),
            'Tags': rest_reverse('api_tags', request=request),
        }

        return Response(data)
    
    def get_view_name(self):
        """
        Change default name
        """
        name = 'Home'
        return name

class ListPosts(APIView):
    """
    API endpoint that allows posts to be viewed
    """
    def get(self, request, format=None):
        """
        Return a list of all posts
        """
        qs = Post.objects.all()
        serialized_data = PostSerializer(qs, many=True)
        return Response(serialized_data.data)
    
class ListTags(APIView):
    """
    API endpoint that allows tags to be viewed
    """
    def  get(self, request, format=None):
        """
        Return a list of all tags
        """
        qs = Tag.objects.all()
        serialized_data = TagSerializer(qs, many=True)
        return Response(serialized_data.data)
