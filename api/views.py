from posts.models import Post
from tags.models import Tag

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse as rest_reverse
from rest_framework import status
from rest_framework import generics

from .serializers import SinglePostSerializer, TagSerializer, PostSerializer
from .permissions import AllowPostOnlyForAuthenticated

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

class ListCreatePosts(generics.ListCreateAPIView):
    """
    API endpoint that allows posts to be viewed and
    created
    """
    permission_classes = [AllowPostOnlyForAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        tag, _ = Tag.objects.get_or_create(name=request.data['tag'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tag=tag, author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_view_name(self):
        """
        Change default name
        """
        name = 'Posts'
        return name
    
class ListCreateTags(generics.ListCreateAPIView):
    """
    API endpoint that allows tags to be viewed and
    created
    """
    permission_classes = [AllowPostOnlyForAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_view_name(self):
        """
        Change default name
        """
        name = 'Tags'
        return name

class SinglePost(APIView):
    """
    API endpoint that allows a single post to be viewed
    """
    def get(self, request, pk, format=None):
        """
        Return the post that corresponds to the provided
        pk
        """
        post = Post.objects.get(pk=pk)
        serialized_data = SinglePostSerializer(post, context={'request': request})
        return Response(serialized_data.data)