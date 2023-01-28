from rest_framework.response import Response
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Annonces,Comments
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from users.models import UserAccount


#posts list,add post view
class AnnonceListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        posts = Annonces.objects.all()
        serializer = AnnonceSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'theme': request.data.get('theme'),
            'modalite': request.data.get('modalite'),
            'category': request.data.get('category'),
            'photo': request.data.get('photo'),
            'tarif': request.data.get('tarif'),
            'lieu': request.data.get('lieu'),
            
        }
        serializer = AnnonceSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#post detail,update post,delete post  
class AnnonceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Annonces.objects.get(pk = pk)
        except Annonces.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = AnnonceSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'theme': request.data.get('theme'),
            'modalite': request.data.get('modalite'),
            'category': request.data.get('category'),
            'photo': request.data.get('photo'),
            'tarif': request.data.get('tarif'),
            'lieu': request.data.get('lieu'),
            
        }
        serializer = AnnonceSerializer(post, data = data, partial = True)
        if serializer.is_valid():
            if post.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error": "You are not authorized to edit this post"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        if post.user.id == request.user.id:
            post.delete()
            return Response({"res": "Object deleted!"}, status = status.HTTP_200_OK)
        return Response({"error": "You are not authorized to delete this post"}, status = status.HTTP_401_UNAUTHORIZED)


#favorite list, add to favorite
class AnnonceFavoriteView(ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        posts = Favorite.objects.get(user=request.user)
        serializer = FavoriteSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args,pk, **kwargs):
        post = self.get_object(pk)
        data = {
            'user': request.user.id,
            'post': post
        }
        serializer = FavoriteSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#history list, add to history
class AnnonceHistoryView(ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        posts = History.objects.get(user=request.user)
        serializer = HistorySerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args,pk, **kwargs):
        post = self.get_object(pk)
        data = {
            'user': request.user.id,
            'post': post
        }
        serializer = HistorySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#search view 
class AnnonceSearchView(APIView):
    serializer_class = AnnonceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends=(SearchFilter,OrderingFilter)
    search_fields=('modalite','category')
    def post(self, request, format=None):
        data = request.data
        category = data['category']
        modalite=data['modalite']
        queryset = Annonces.objects.filter(category__iexact=category,modalite__iexact=modalite)

        serializer = AnnonceSerializer(queryset, many=True)

        return Response(serializer.data)

#comments list, add comment
class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Annonces.objects.get(pk = pk)
        except Annonces.DoesNotExist:
            return None
    
    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        comments = Comments.objects.filter(post = post)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user.id,
            'post': post.id,
            'body': request.data.get('body')
        }
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#user posts 
class UserAnnonceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk, *args, **kwargs):
        user = UserAccount.objects.filter(pk =pk).first()
        if user is None:
            return Response({'error': 'User not found'}, status = status.HTTP_404_NOT_FOUND)
        posts = Annonces.objects.filter(user = user)
        serializer = AnnonceSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


