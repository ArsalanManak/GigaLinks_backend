from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth as auth_router
from .api import media as media_router
from .core import config

# rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# security middleware
from .middleware.security import SecurityHeadersMiddleware

app = FastAPI(title="GigaLinks API")

# Configure CORS from env-config
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach security headers
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
# simple handler mapping for rate limit exceeded
def _rl_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})

app.add_exception_handler(RateLimitExceeded, _rl_handler)


@app.get("/")
async def root():
    return {"message": "GigaLinks API is running"}


app.include_router(auth_router.router)
app.include_router(media_router.router)
from .api import projects as projects_router
from .api import services as services_router
from .api import inquiries as inquiries_router

app.include_router(projects_router.router)
app.include_router(services_router.router)
app.include_router(inquiries_router.router)
