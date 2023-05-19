from app.domain.entities.users.model.user_model import Users

from ..services.base_service import BaseService


class UsersService(BaseService):
    model = Users