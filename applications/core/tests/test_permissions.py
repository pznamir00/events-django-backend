from unittest.mock import MagicMock
from applications.core.permissions import CreateAuthenticatedOnly, IsOwnerOrReadOnly


class TestIsOwnerOrReadOnly:
    def test_has_object_permission_returns_true_if_method_is_safe(self):
        permission = IsOwnerOrReadOnly()
        user = MagicMock(email="admin@gmail.com", is_superuser=True)
        other_user = MagicMock(email="test@gmail.com")
        req = MagicMock(method="GET", user=user)
        obj = MagicMock(promoter=other_user)
        assert permission.has_object_permission(req, None, obj)  # type: ignore

    def test_has_object_permission_returns_true_if_user_is_superuser(self):
        permission = IsOwnerOrReadOnly()
        user = MagicMock(email="admin@gmail.com", is_superuser=True)
        other_user = MagicMock(email="test@gmail.com")
        req = MagicMock(method="POST", user=user)
        obj = MagicMock(promoter=other_user)
        assert permission.has_object_permission(req, None, obj)  # type: ignore

    def test_has_object_permission_returns_true_if_user_is_owner(self):
        permission = IsOwnerOrReadOnly()
        user = MagicMock(email="test@gmail.com", is_superuser=False)
        req = MagicMock(method="POST", user=user)
        obj = MagicMock(promoter=user)
        assert permission.has_object_permission(req, None, obj)  # type: ignore

    def test_has_object_permission_returns_false_if_user_is_either_not_superuser_or_owner(
        self,
    ):
        permission = IsOwnerOrReadOnly()
        user = MagicMock(email="user@gmail.com", is_superuser=False)
        other_user = MagicMock(email="test@gmail.com")
        req = MagicMock(method="POST", user=user)
        obj = MagicMock(promoter=other_user)
        assert not permission.has_object_permission(req, None, obj)  # type: ignore


class TestCreateAuthenticatedOnly:
    def test_has_permission_returns_true_if_method_is_not_post(self):
        permission = CreateAuthenticatedOnly()
        user = MagicMock(email="test@gmail.com", is_authenticated=False)
        req = MagicMock(method="GET", user=user)
        assert permission.has_permission(req, None)  # type: ignore

    def test_has_permission_returns_true_if_method_is_post_and_user_is_authenticated(
        self,
    ):
        permission = CreateAuthenticatedOnly()
        user = MagicMock(email="test@gmail.com", is_authenticated=True)
        req = MagicMock(method="POST", user=user)
        assert permission.has_permission(req, None)  # type: ignore

    def test_has_permission_returns_false_if_method_is_post_and_user_is_not_authenticated(
        self,
    ):
        permission = CreateAuthenticatedOnly()
        user = MagicMock(email="test@gmail.com", is_authenticated=False)
        req = MagicMock(method="POST", user=user)
        assert not permission.has_permission(req, None)  # type: ignore
