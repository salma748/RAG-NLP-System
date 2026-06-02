from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from controllers.NlpController import (
    NlpController
)

from models.ProjectModel import (
    ProjectModel
)

from routes.schema.nlp import (
    SearchRequest
)


nlp_router = APIRouter(
    prefix="/api/nlp",
    tags=["nlp"]
)


def get_nlp_controller(
    request: Request
):

    return NlpController(

        vectordb_client=(
            request.app.vectordb_client
        ),

        generation_client=(
            request.app.generation_client
        ),

        embedding_client=(
            request.app.embedding_client
        ),

        template_parser=(
            request.app.template_parser
        ),
    )


# Push To Index

@nlp_router.post("/index/push/{project_id}")
async def push_to_index(
    project_id: str,
    request: Request
):

    project_model = ProjectModel(
        request.app.db_client
    )

    project = await project_model.get_project(
        project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    nlp_controller = (
        get_nlp_controller(request)
    )

    # Controller handles:
    # - chunk retrieval
    # - pagination / batching
    # - embeddings generation
    # - upload to Qdrant

    await nlp_controller.push_data_to_index(
        project=project,
        db_client=request.app.db_client
    )

    return {
        "message": (
            "Chunks indexed successfully"
        )
    }


# Semantic Search

@nlp_router.post("/index/search/{project_id}")
async def search_by_vector(
    project_id: str,
    search_request: SearchRequest,
    request: Request
):

    project_model = ProjectModel(
        request.app.db_client
    )

    project = await project_model.get_project(
        project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    results = (
        get_nlp_controller(request)
        .search_by_vector(
            project=project,
            text=search_request.text,
            top_k=search_request.top_k,
        )
    )

    if not results:

        return {

            "results": [],

            "message": (
                "No matching chunks found."
            )
        }

    return {
        "results": results
    }


# Generate RAG Answer

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(
    project_id: str,
    search_request: SearchRequest,
    request: Request
):

    project_model = ProjectModel(
        request.app.db_client
    )

    project = await project_model.get_project(
        project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    result = (
        get_nlp_controller(request)
        .answer_rag_question(
            project=project,
            query=search_request.text,
            top_k=search_request.top_k,
        )
    )

    return result