# Tenzro Python SDK

Official Python SDK for interacting with the Tenzro API.

## Installation

```bash
pip install tenzro
```

## Usage

```python
from tenzro import Client

async with Client(api_key="your-api-key", nid="node-id") as client:
    # Create a training job
    job = await client.jobs.create(
        type="training",
        model="custom-model",
        config={
            "epochs": 100,
            "batch_size": 32
        }
    )
    print(f"Created job: {job.id}")

    # Get job status
    job_status = await client.jobs.get(job.id)
    print(f"Job status: {job_status.status}")

    # List jobs
    jobs = await client.jobs.list(limit=10, offset=0)
    print(f"Total jobs: {len(jobs)}")

    # Cancel job
    cancelled_job = await client.jobs.cancel(job.id)
    print(f"Cancelled job: {cancelled_job.id}")
```

## API Reference

### Client

```python
Client(api_key: str, nid: str)
```

### Jobs

- `create(type: str, model: str, config: Dict[str, Any]) -> Job`
- `get(job_id: str) -> Job`
- `list(limit: int = 10, offset: int = 0) -> Dict[str, Any]`
- `cancel(job_id: str) -> Job`

## License

MIT License