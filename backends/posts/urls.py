from django.urls import include,path
from .views import *


urlpatterns = [
    #posts list 
    path('', AnnonceListAPIView.as_view(), name='AnnonceList'),
    #add annonce
    path('add/', AnnonceAPIView.as_view(), name='Add Annonce'),
    #post detail 
    path('<int:pk>/', AnnonceDetailAPIView.as_view(), name='AnnonceDetail'),
    #post comments  
    path('<int:pk>/comment/', CommentAPIView.as_view(), name='comments'),
    #user posts
    path('<email>/', UserAnnonceAPIView.as_view(), name='userposts'),
    #favorite list
    path('<int:pk>/favorite/', AnnonceFavoriteView.as_view(), name='favoriteList'),
    #search list 
    path('category/', AnnonceSearchView.as_view(), name='category')
]