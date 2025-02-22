import logging
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from logic.router import api_router

from core.config import settings, telex_integration_config
from core.settings import get_dynamic_settings, extract_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv(".env")

app = FastAPI(
    title="Vivace Integration API",
    description="API for the Vivace Integration",
    version="0.0.1",
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

dynamic_settings = get_dynamic_settings(
    count=1,
    types=["text"],
    labels=["Knowledge Base URL(separate multiple sources with commas)"],
    descriptions=["URL(s) for the knowledge base."],
    defaults=["https://aws.amazon.com/what-is/retrieval-augmented_generation/"],
    required=[True],
    options=[None],
)


@app.get("/")
async def load_home():
    """
    Loads the home page.
    """
    logger.info("Loading home page")
    return JSONResponse(
        {"code": 200, "message": "Vivace Telex Integration", "status": 200}
    )


@app.get("/integration_setting")
async def load_settings(request: Request):
    """
    Loads settings from a JSON file.

    Returns:
        JSONResponse: The loaded settings.

    Raises:
        HTTPException: If the file is not found or the JSON is invalid.
    """
    logger.info("Loading integration settings")
    body = await request.body()
    if body:
        logger.info(f"Received data: {body.decode('utf-8')}")
    try:

        telex_integration_config["data"]["settings"] = dynamic_settings
        return JSONResponse(telex_integration_config)
    except Exception as e:
        logger.error(f"Error loading integration settings: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# @app.post("/update_settings")
# async def update_settings(request: Request):
#     """
#     Updates the settings based on the content of the input request.

#     Receives a JSON payload and updates the settings.
#     """
#     try:
#         data = await request.json()
#         logger.info(f"Received request data: {data}")

#         settings_list = data.get("settings", [])
#         if not settings_list:
#             raise HTTPException(
#                 status_code=400, detail="Missing 'settings' in request body"
#             )

#         updated_settings = extract_settings(settings_list)
#         logger.info(f"Updated settings: {updated_settings}")

#         # Update the global dynamic_settings
#         global dynamic_settings
#         dynamic_settings = get_dynamic_settings(
#             count=len(settings_list),
#             types=[setting["type"] for setting in settings_list],
#             labels=[setting["label"] for setting in settings_list],
#             descriptions=[setting.get("description", "") for setting in settings_list],
#             defaults=[setting["default"] for setting in settings_list],
#             required=[setting["required"] for setting in settings_list],
#             options=[setting.get("options", None) for setting in settings_list],
#         )

#         return JSONResponse({"status": "success", "updated_settings": updated_settings})
#     except HTTPException as e:
#         logger.exception(f"HTTPException: {e}")
#         raise e
#     except Exception as e:
#         logger.exception("An unexpected error occurred")
#         return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/healthcheck")
async def health_check():
    """Checks if server is active."""
    logger.info("Performing health check")
    return {"status": "active"}


@app.get("/logo.png")
async def get_logo():
    """
    Serves the Vivace logo image.

    Returns:
        FileResponse: The PNG image file.
    """
    logger.info("Serving logo image")
    logo_path = "./assets/vivace_logo.png"
    return FileResponse(logo_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
