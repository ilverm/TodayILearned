from posts.models import Post
from tags.models import Tag

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse as rest_reverse
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import status
from rest_framework import generics

from .serializers import SinglePostSerializer, TagSerializer, PostSerializer

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
    
class SinglePost(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single post to be viewed,
    updated or deleted.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Post.objects.all()
    serializer_class = SinglePostSerializer
    lookup_field = 'pk'
    
class ListCreateTags(generics.ListCreateAPIView):
    """
    API endpoint that allows tags to be viewed and
    created
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Tag.objects.all().order_by('-created_at')
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_view_name(self):
        """
        Change default name
        """
        name = 'Tags'
        return name
    
class SingleTag(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a single tag to be viewed,
    updated or deleted.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'pk'
    