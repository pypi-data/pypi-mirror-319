# tenzro/jobs.py
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(BaseModel):
    id: str
    type: str
    model: str
    status: JobStatus
    config: Dict[str, Any]
    created_at: str
    updated_at: str

class Jobs:
    def __init__(self, client):
        self.client = client

    async def create(
        self,
        type: str,
        model: str,
        config: Dict[str, Any]
    ) -> Job:
        response = await self.client._request(
            "POST",
            "/jobs",
            json={
                "type": type,
                "model": model,
                "config": config,
            },
        )
        return Job(**response)

    async def get(self, job_id: str) -> Job:
        response = await self.client._request("GET", f"/jobs/{job_id}")
        return Job(**response)

    async def list(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        return await self.client._request(
            "GET",
            "/jobs",
            params={"limit": limit, "offset": offset},
        )

    async def cancel(self, job_id: str) -> Job:
        response = await self.client._request("POST", f"/jobs/{job_id}/cancel")
        return Job(**response)