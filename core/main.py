from fastapi import FastAPI
from core.routes.users import router as router_users
from core.routes.salary import router as router_salaries
from core.routes.login import router as router_login


app = FastAPI()
app.include_router(router_users)
app.include_router(router_salaries)
app.include_router(router_login)
