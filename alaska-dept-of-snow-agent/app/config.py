import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_ID = os.getenv("PROJECT_ID", "")
    LOCATION = os.getenv("LOCATION", "us-central1")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.2-flash")

    GCS_BUCKET = os.getenv("GCS_BUCKET", "labs.roitraining.com")
    GCS_PREFIX = os.getenv("GCS_PREFIX", "alaska-dept-of-snow")

    LOG_DATASET = os.getenv("LOG_DATASET", "ads_agent_logs")
    LOG_TABLE = os.getenv("LOG_TABLE", "prompt_response_logs")

    MODEL_ARMOR_TEMPLATE_ID = os.getenv("MODEL_ARMOR_TEMPLATE_ID", "ads-safety-template")
    MODEL_ARMOR_LOCATION = os.getenv("MODEL_ARMOR_LOCATION", "us-central1")

settings = Settings()