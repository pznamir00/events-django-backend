from unittest.mock import MagicMock
import pytest
from applications.tickets.permissions import IsOwner


class TestIsOwnerPermission:
    @pytest.fixture(autouse=True)
    def req(self):
        req = MagicMock()
        req.user = {"email": "test@gamil.com"}
        return req

    @pytest.fixture(autouse=True)
    def obj(self):
        return MagicMock()

    def test_has_object_permission_returns_true_if_promoter_is_user(
        self, req: MagicMock, obj: MagicMock
    ):
        permission = IsOwner()
        obj.promoter = {"email": "test@gamil.com"}
        assert permission.has_object_permission(req, None, obj)

    def test_has_object_permission_returns_false_if_promoter_is_not_user(
        self, req: MagicMock, obj: MagicMock
    ):
        permission = IsOwner()
        obj.promoter = {"email": "other@gamil.com"}
        assert not permission.has_object_permission(req, None, obj)
