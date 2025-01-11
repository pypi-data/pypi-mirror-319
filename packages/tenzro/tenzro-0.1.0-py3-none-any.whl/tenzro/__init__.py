# tenzro/__init__.py
from .client import Client
from .jobs import Job, JobStatus

__all__ = ["Client", "Job", "JobStatus"]
__version__ = "0.1.0"

# tenzro/client.py
import aiohttp
from typing import Optional, Dict, Any
from .jobs import Jobs

class Client:
    BASE_URL = "https://api.tenzro.com/v0"

    def __init__(self, api_key: str, nid: str):
        self.api_key = api_key
        self.nid = nid
        self.session = None
        self.jobs = Jobs(self)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-Node-ID": self.nid,
                "Content-Type": "application/json",
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-Node-ID": self.nid,
                    "Content-Type": "application/json",
                }
            )
        
        async with self.session.request(method, f"{self.BASE_URL}{path}", **kwargs) as response:
            response.raise_for_status()
            return await response.json()