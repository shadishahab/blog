from rest_framework import serializers

from users.serializers import UserDetailSerializer

from .models import Comment, Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['written_by']
    def create(self, validated_data):
        validated_data['written_by'] = self.context['request'].user
        return super().create(validated_data)


class PostReadSerializer(serializers.ModelSerializer):
    written_by = UserDetailSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = '__all__'


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'tags', 'content']


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', 'written_by']
    def create(self, validated_data):
        validated_data['written_by'] = self.context['request'].user
        return super().create(validated_data)
    

class CommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['post']