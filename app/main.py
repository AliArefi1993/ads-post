from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import auth, ads, user, comment


app = FastAPI()


# authentication
app.include_router(auth.router)

# ads
app.include_router(ads.router)


# user
app.include_router(user.router)

# comment
app.include_router(comment.router)
