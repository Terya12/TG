from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from config import settings


class AdminAuth(AuthenticationBackend):
    def __init__(self):
        super().__init__(secret_key=settings.secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == settings.admin and password == settings.admin_password:
            request.session.update({"token": "authenticated"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("token") == "authenticated"
