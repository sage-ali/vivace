from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from logic.router import api_router

from core.config import settings, telex_integration_config

# Load environment variables from .env file
load_dotenv(".env")

app = FastAPI(
    title="Vivace Integration API",
    description="API for the Vivace Integration",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
async def load_home():
    """
    Loads the home page.
    """
    return JSONResponse({"code":200,"message":"Vivace Telex Integration","status":200})

@app.get("/integration_setting")
async def load_settings():
    """
    Loads settings from a JSON file.

    Returns:
        dict: The loaded settings.

    Raises:
        HTTPException: If the file is not found or the JSON is invalid.
    """
    return JSONResponse(telex_integration_config)


@app.get("/healthcheck")
async def health_check():
    """Checks if server is active."""
    return {"status": "active"}

@app.get("/logo.png")
async def get_logo():
    """
    Serves the Vivace logo image.

    Returns:
        FileResponse: The SVG image file.
    """
    logo_path = "./assets/vivace_logo.png"
    return FileResponse(logo_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)