from fastapi import (
    APIRouter,
    UploadFile,
    Request,
    HTTPException,
)

from fastapi.responses import JSONResponse

import aiofiles
import os

from controllers.DataController import DataController
from controllers.FileController import FileController
from controllers.ProcessController import ProcessController

from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel

from helpers.config import Settings


data_router = APIRouter(
    prefix="/api/data",
    tags=["data"]
)


# =========================
# Test Endpoint
# =========================
@data_router.get("/")
async def test_data():

    return {
        "message": "Data router working"
    }


# =========================
# Upload Endpoint
# =========================
@data_router.post("/upload/{project_id}")

async def upload_file(
    request: Request,
    project_id: str,
    files: list[UploadFile]
):

    settings = Settings()

    # MongoDB project model
    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    # Create or get project
    await project_model.get_project_or_create_one(
        project_id
    )

    uploaded_files = []

    # Loop through uploaded files
    for file in files:

        # Validate uploaded file
        is_valid, error_msg = (
            DataController().validate_file(file)
        )

        if not is_valid:

            return JSONResponse(
                status_code=400,
                content={
                    "error":
                    f"{file.filename}: {error_msg}"
                }
            )

        # Generate file path
        file_path = FileController().get_file_path(
            project_id=project_id,
            filename=file.filename
        )

        # Save file asynchronously
        async with aiofiles.open(
            file_path,
            "wb"
        ) as out_file:

            while chunk := await file.read(
                settings.FILE_CHUNK_SIZE
            ):

                await out_file.write(chunk)

        uploaded_files.append(
            file.filename
        )

    return {
        "message": "files uploaded successfully",
        "project_id": project_id,
        "uploaded_files": uploaded_files
    }

# =========================
# Process Documents Endpoint
# =========================
@data_router.post("/process/{project_id}")
async def process_documents(
    request: Request,
    project_id: str
):

    process_controller = ProcessController()

    chunk_model = ChunkModel(
        db_client=request.app.db_client
    )

    project_model = ProjectModel(
        db_client=request.app.db_client
    )

    # Check if project exists
    project = await project_model.get_project(
        project_id
    )

    if not project:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # Project files directory
    project_path = os.path.join(
        "assets/files",
        project_id
    )

    # Check if folder exists
    if not os.path.exists(project_path):

        raise HTTPException(
            status_code=404,
            detail="Project files folder not found"
        )

    # Delete old chunks before reprocessing
    await chunk_model.delete_chunks_by_project_id(
        project_id
    )

    all_chunks = []

    # Loop through files
    for filename in os.listdir(project_path):

        # Process only HTML files
        if not filename.endswith(".html"):
            continue

        file_path = os.path.join(
            project_path,
            filename
        )

        try:

            # Read & clean HTML content
            text = process_controller.get_file_content(
                file_path=file_path
            )

            # Skip empty files
            if not text:
                continue

            # Generate chunks
            chunks = process_controller.process_files(
                text=text,
                chunk_size=400,
                overlap=40,
            )

            # Skip empty chunks
            if not chunks:
                continue

            # Add chunks to global list
            all_chunks.extend(chunks)

        except Exception as error:

            print(
                f"Failed processing file: {filename}"
            )

            print(error)

    # Insert chunks into MongoDB
    inserted_chunks = await chunk_model.insert_many_chunks(
        project_id=project_id,
        chunks=all_chunks
    )

    return {
        "message": "documents processed successfully",
        "project_id": project_id,
        "total_chunks": inserted_chunks,
        "processed_files": len(os.listdir(project_path)),
    }