from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from routes.base import base_router
from routes.data import data_router
from routes.nlp import nlp_router
from stores.llm.LLMFactory import LLMFactory
from stores.llm.tempelate.template_parser import TemplateParser
from stores.vectordb.VectorDBFactory import VectorDBFactory

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# Routers
app.include_router(base_router)
app.include_router(data_router)
app.include_router(nlp_router)


@app.on_event("startup")
async def startup():

    try:
        # MongoDB
        mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)

        app.mongo_client = mongo_client
        app.db_client = mongo_client[settings.MONGODB_DB_NAME]

        print(" MongoDB connected")


        # Embedding Model
        app.embedding_client = LLMFactory.create(
            "local_bge",
            model_name=settings.EMBEDDINGS_MODEL,
        )

        print("Embedding model loaded")


        # Generation Model
        app.generation_client = LLMFactory.create(
            "openai",
            api_key=settings.OPENAI_API_KEY,
            api_base=settings.OPENAI_API_BASE,
            model_name=settings.GENERATE_RESPONSE_MODEL,
            max_response_tokens=settings.MAX_RESPONSE_TOKENS,
            temperature=settings.TEMPERATURE,
        )

        print(" Generation model initialized")


        # Qdrant
        app.vectordb_client = VectorDBFactory.create(
            "qdrant",
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            distance_metric=settings.VECTOR_DISTANCE_METRIC,
        )

        print("Qdrant connected")


        # Template Parser
        app.template_parser = TemplateParser(language="en")

        print(" Template parser loaded")


    except Exception as e:
        print(f"Startup Error: {e}")


@app.on_event("shutdown")
async def shutdown():

    app.mongo_client.close()

    print(" MongoDB connection closed")


@app.get("/")
async def home():

    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }