from django.urls import include,path
from .views import *


urlpatterns = [
    #posts list 
    path('', AnnonceListAPIView.as_view(), name='AnnonceList'),
    #add annonce
    path('add/', AnnonceAPIView.as_view(), name='Add Annonce'),
    #post detail 
    path('<int:pk>/', AnnonceDetailAPIView.as_view(), name='AnnonceDetail'),
    #edit post
    path('<int:pk>/edit/', AnnonceUpdate.as_view(), name='EditAnnonce'),
    #delete post
    path('<int:pk>/delete/', AnnonceDelete.as_view(), name='DeleteAnnonce'),
    #post comments  
    path('<int:pk>/comment/', CommentAPIView.as_view(), name='Comments'),
    #add comments 
    path('<int:pk>/addcomment/', AddCommentAPIView.as_view(), name='AddComments'),
    #user posts
    path('<email>/', UserAnnonceAPIView.as_view(), name='UserPosts'),
    #favorite list
    path('favorite/', AnnonceFavoriteView.as_view(), name='FavoriteList'),
    #add favorite
    path('<int:pk>/favorite/', AddFavorite.as_view(), name='AddFavorite'),
    #search list 
    path('category/', AnnonceSearchView.as_view(), name='category')
]