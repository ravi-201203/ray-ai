import json
import os
from fastapi import APIRouter, HTTPException
import ray

from config.logger import logger
from model.models import (
    BatchTariffCalculationRequest,
    TariffEvaluationFailure,
    TariffEvaluationSuccess,
)

# -------------------------
# Ray + FastAPI setup
# -------------------------
rayRosteringRouter = APIRouter()

ray.init(ignore_reinit_error=True)

# -------------------------
# Load rules ONCE (BIG WIN)
# -------------------------
try:
    with open("rules/MIZO-FY-24-25.json") as f:
        MODEL = json.load(f)
except FileNotFoundError:
    raise RuntimeError("Rules file missing at startup")

# -------------------------
# Ray Actor (engine reused)
# -------------------------
@ray.remote
class TariffActor:
    def __init__(self, model):
        from zen import ZenEngine
        self.engine = ZenEngine()
        self.decision = self.engine.create_decision(model)

    def process_chunk(self, chunk):
        success_results = []
        failed_results = []

        for single_req in chunk:
            # faster than .dict()
            context = single_req.__dict__
            try:
                result = self.decision.evaluate(context)
                success_results.append(
                    TariffEvaluationSuccess(result=result)
                )
            except Exception as e:
                failed_results.append(
                    TariffEvaluationFailure(
                        context=context,
                        error=str(e)
                    )
                )

        return success_results, failed_results


# -------------------------
# Chunk helper
# -------------------------
def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


# -------------------------
# Create actors once
# -------------------------
CPU_COUNT = os.cpu_count() or 4
ACTORS = [TariffActor.remote(MODEL) for _ in range(CPU_COUNT)]


# -------------------------
# FastAPI endpoint
# -------------------------
@rayRosteringRouter.post("/evaluate/batch/parallel")
async def evaluateTariffBatchparallel(req: BatchTariffCalculationRequest):

    total_requests = len(req.requests)
    logger.info(f"Batch tariff evaluation invoked, count={total_requests}")

    if total_requests == 0:
        return {
            "summary": {
                "total_requests": 0,
                "chunks_processed": 0,
                "succeeded": 0,
                "failed": 0,
            },
            "success": [],
            "failed": [],
        }

    # Tune chunk size
    CHUNK_SIZE = 500
    chunks = list(chunk_list(req.requests, CHUNK_SIZE))

    logger.info(
        f"Chunks={len(chunks)}, "
        f"Actors={len(ACTORS)}, "
        f"ChunkSize={CHUNK_SIZE}"
    )

    # Dispatch chunks round-robin to actors
    futures = [
        ACTORS[i % len(ACTORS)].process_chunk.remote(chunk)
        for i, chunk in enumerate(chunks)
    ]

    # Collect results (parallel underneath)
    results = ray.get(futures)

    success_results = []
    failed_results = []

    for s, f in results:
        success_results.extend(s)
        failed_results.extend(f)

    return {
        "summary": {
            "total_requests": total_requests,
            "chunks_processed": len(chunks),
            "succeeded": len(success_results),
            "failed": len(failed_results),
        },
        "success": success_results,
        "failed": failed_results,
    }
