from fastapi import Depends, Request

from core.dependencies.database import get_db_op
from core.dependencies.locale import gettext_translator


def get_current_user(request: Request) -> dict:
    if hasattr(request.state, 'jwt_info'):
        return request.state.jwt_info
        # {
        #   "id":"user_id",
        #   "username":"username"}
    return {}


def require_permissions(required_perms: list[str],
                        user=Depends(get_current_user),
                        db=Depends(get_db_op),
                        _=Depends(gettext_translator)):
    # 鉴权逻辑待添加
    # if not any(perm in user.permissions for perm in required_perms):
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, _("You don't have permission to perform this action"))
    return user
