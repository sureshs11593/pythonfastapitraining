import time
import uuid

JOB_DURATION_SECONDS = 3.0


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, dict] = {}

    def enqueue(self, payload: dict) -> str:
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        self._jobs[job_id] = {"id": job_id, "created_at": time.monotonic(), "payload": payload}
        return job_id

    def get(self, job_id: str) -> dict | None:
        job = self._jobs.get(job_id)
        if not job:
            return None
        elapsed = time.monotonic() - job["created_at"]
        #time.monotoic() returns the current time from a monotonic clock
        #job["created_at"] stores when the job was enqueued
        # subtracting them gives the elapsed time since the job was created
        if elapsed >= JOB_DURATION_SECONDS:
            return {"id": job_id, "status": "done", "result_url": f"/day4/reports/{job_id}/result"}
        return {"id": job_id, "status": "pending", "result_url": None}


job_store = JobStore()
