from fastapi import FastAPI

from core.config import settings
from core.setup.app import create_app

app = create_app()

def show_routes(_app:FastAPI):
    for route in _app.routes:
        if hasattr(route, "methods"):
            print(f"HTTP Route: {list(route.methods)[0].ljust(6)}\t{route.path}")
        elif hasattr(route, "path"):
            print(f"Static/Mount Route: {route.path}")


if __name__ == "__main__":
    import uvicorn
    show_routes(app)
    uvicorn.run(
        "main:app",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        # reload=settings.uvicorn.reload,
        # reload_dirs=settings.uvicorn.reload_dirs,
        # reload_includes=settings.uvicorn.reload_includes,
        # reload_excludes=settings.uvicorn.reload_excludes,
        log_level=settings.uvicorn.log_level,
        workers=settings.uvicorn.workers
    )