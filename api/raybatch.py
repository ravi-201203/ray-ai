import json
from fastapi import APIRouter, HTTPException
import ray

from config.logger import logger
from model.models import BatchTariffCalculationRequest, TariffEvaluationFailure, TariffEvaluationSuccess


rayRosteringRouter = APIRouter()

ray.init()


@ray.remote
def process_chunk_ray(chunk, model):
    from zen import ZenEngine
    engine = ZenEngine()
    decision = engine.create_decision(model)

    success_results = []
    failed_results = []

    for single_req in chunk:
        context = single_req.dict()
        try:
            result = decision.evaluate(context)
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

def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


@rayRosteringRouter.post("/evaluate/batch/parallel")
async def evaluateTariffBatchparallel(req: BatchTariffCalculationRequest):

    logger.info(f"Batch tariff evaluation invoked, count={len(req.requests)}")

    # Load rules
    try:
        with open("rules/MIZO-FY-24-25.json") as f:
            model = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Rules file missing")

    CHUNK_SIZE = 500
    chunks = list(chunk_list(req.requests, CHUNK_SIZE))

    logger.info(f"Total chunks: {len(chunks)}")

    # Launch Ray tasks (true parallelism)
    ray_tasks = [
        process_chunk_ray.remote(chunk, model)
        for chunk in chunks
    ]

    # Collect results (blocking but parallel underneath)
    results = ray.get(ray_tasks)

    success_results = []
    failed_results = []

    for s, f in results:
        success_results.extend(s)
        failed_results.extend(f)

    return {
        "summary": {
            "total_requests": len(req.requests),
            "chunks_processed": len(chunks),
            "succeeded": len(success_results),
            "failed": len(failed_results),
        },
        "success": success_results,
        "failed": failed_results,
    }

