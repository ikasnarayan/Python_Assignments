from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.file_reader import read_file, read_multiple_files

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/read")
def read_single(file_path: str, background_tasks: BackgroundTasks):
    try:
        if not file_path or not isinstance(file_path, str):
            raise HTTPException(status_code=400, detail="Invalid file path provided")

        background_tasks.add_task(read_file, file_path)
        return {"status": "Reading started", "file": file_path}

    except HTTPException as he:
        # re-raise known errors
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while scheduling file read: {e}")


@router.post("/read-multiple")
def read_multiple(files: list[str], background_tasks: BackgroundTasks):
    try:
        if not files or not isinstance(files, list):
            raise HTTPException(status_code=400, detail="Files list must be provided")
        if not all(isinstance(f, str) for f in files):
            raise HTTPException(status_code=400, detail="All file paths must be strings")

        background_tasks.add_task(read_multiple_files, files)
        return {"status": f"Started reading {len(files)} files"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while scheduling multiple file reads: {e}")
