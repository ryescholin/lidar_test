# main.py
import uvicorn
import asyncio
from app import app
from camera import camera_go

config = uvicorn.Config(
    "app:app",
    host = "0.0.0.0",
    port=8000,
    log_level="info",
    access_log=True,
    use_colors=True,
    reload=True,
)
server = uvicorn.Server(config)

async def main() -> None:
    await asyncio.gather(server.serve(), camera_go(), return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())