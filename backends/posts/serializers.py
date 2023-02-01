from rest_framework import serializers
from .models import *
#posts serializer
class AnnonceSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source = 'user.first_name')
  class Meta:
        model = Annonces
        fields = '__all__'
    
#comments serializer
class CommentSerializer(serializers.ModelSerializer):
  user = serializers.ReadOnlyField(source = 'user.first_name')
  class Meta:
        model = Comments
        fields = '__all__'


#favorite serializer
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'




