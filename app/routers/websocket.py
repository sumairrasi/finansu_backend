from fastapi import APIRouter, WebSocket
from celery.result import AsyncResult
from app.background.worker import celery_app
import asyncio

router = APIRouter()


@router.websocket("/ws/progress/{task_id}")
async def task_progress(websocket: WebSocket, task_id: str):
    await websocket.accept()

    while True:
        task_result = AsyncResult(task_id, app=celery_app)

        if task_result.state == "PENDING":
            await websocket.send_json({
                "state": "PENDING",
                "percentage": 0
            })

        elif task_result.state == "PROGRESS":
            meta = task_result.info or {}
            await websocket.send_json({
                "state": "PROGRESS",
                "percentage": meta.get("percentage", 0),
                "current": meta.get("current", 0),
                "total": meta.get("total", 0),
                "current_file": meta.get("current_file", "")
            })

        elif task_result.state == "SUCCESS":
            await websocket.send_json({
                "state": "SUCCESS",
                "percentage": 100,
                "result": task_result.result
            })
            break

        elif task_result.state == "FAILURE":
            await websocket.send_json({
                "state": "FAILURE",
                "error": str(task_result.info)
            })
            break

        await asyncio.sleep(1)

    await websocket.close()
