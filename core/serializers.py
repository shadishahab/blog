from rest_framework import serializers
from .models import Tag, Post, Comment
from users.serializers import UserDetailSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['written_by']
    def create(self, validated_data):
        validated_data['written_by'] = self.context['request'].user
        return super().create(validated_data)


class PostReadSerializer(serializers.ModelSerializer):
    written_by = UserDetailSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        exclude = ['content']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'content']