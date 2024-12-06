from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.models import CustomUser

from .models import Comment, Post, Tag

# Model Unit Tests
class BaseTestCase(APITestCase):
    def authenticate_user(self, user):
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


class PostModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="author", password="password123", role="author"
        )
        self.post = Post.objects.create(
            title="Test Post", content="This is a test post.", written_by=self.user
        )
        self.tag = Tag.objects.create(name="Django")

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.written_by, self.user)
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)

    def test_post_string_representation(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_post_tags(self):
        self.post.tags.add(self.tag)
        self.assertIn(self.tag, self.post.tags.all())


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="reader", password="password123", role="reader"
        )
        self.post = Post.objects.create(
            title="Another Post", content="Testing comments.", written_by=self.user
        )
        self.comment = Comment.objects.create(
            content="Nice post!", written_by=self.user, post=self.post
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Nice post!")
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.written_by, self.user)
        self.assertIsNotNone(self.comment.timestamp)

    def test_comment_string_representation(self):
        self.assertEqual(str(self.comment), f"Comment by {self.user.username} on {self.post.title}")


class TagModelTests(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Test Tag")

    def test_tag_string_representation(self):
        self.assertEqual(str(self.tag), "Test Tag")


# Integration Tests
class PostTests(BaseTestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username="admin", password="password123", role="admin"
        )
        self.author_user = CustomUser.objects.create_user(
            username="author", password="password123", role="author"
        )
        self.reader_user = CustomUser.objects.create_user(
            username="reader", password="password123", role="reader"
        )

        self.tag = Tag.objects.create(name="Django")
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            written_by=self.author_user,
        )
        self.post.tags.add(self.tag)

    def test_post_creation_by_author(self):
        self.authenticate_user(self.author_user)
        url = reverse("post-create")
        data = {"title": "New Post", "content": "New content", "tags": [self.tag.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_creation_by_reader_forbidden(self):
        self.authenticate_user(self.reader_user)
        url = reverse("post-create")
        data = {"title": "Reader's Post", "content": "Reader's content"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_list(self):
        self.client.force_authenticate(user=self.reader_user)
        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_post_update_by_owner(self):
        self.client.force_authenticate(user=self.author_user)
        url = reverse("post-update", kwargs={"pk": self.post.id})
        data = {"title": "Updated Title", "content": "Updated Content"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_post_update_by_non_owner_forbidden(self):
        self.client.force_authenticate(user=self.reader_user)
        url = reverse("post-update", kwargs={"pk": self.post.id})
        data = {"title": "New Title"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_by_admin(self):
        self.authenticate_user(self.admin_user)
        url = reverse("post-delete", kwargs={"pk": self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTests(BaseTestCase):
    def setUp(self):
        self.author_user = CustomUser.objects.create_user(
            username="author", password="password123", role="author"
        )
        self.reader_user = CustomUser.objects.create_user(
            username="reader", password="password123", role="reader"
        )

        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            written_by=self.author_user,
        )
        self.comment = Comment.objects.create(
            content="This is a test comment.",
            post=self.post,
            written_by=self.reader_user,
        )

    def test_comment_creation_by_reader(self):
        self.authenticate_user(self.reader_user)
        url = reverse("comment-create", kwargs={"post_pk": self.post.id})
        data = {"content": "A new comment"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_creation_by_unauthenticated_user(self):
        url = reverse("comment-create", kwargs={"post_pk": self.post.id})
        data = {"content": "A comment by unauthenticated user"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_list(self):
        self.client.force_authenticate(user=self.author_user)
        url = reverse("comment-list", kwargs={"post_pk": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], self.comment.content)
