import json
import ray
from zen import ZenEngine  # your existing engine


@ray.remote
class TariffEvaluatorActor:
    def __init__(self, rules: dict):
        self.engine = ZenEngine()
        self.decision = self.engine.create_decision(rules)

    def evaluate(self, context):
        import time
        time.sleep(1)

        return self.decision.evaluate(context)
