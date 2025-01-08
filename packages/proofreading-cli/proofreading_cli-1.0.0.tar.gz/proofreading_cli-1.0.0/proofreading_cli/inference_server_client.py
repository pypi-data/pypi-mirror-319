import json
import os
from typing import Any, Tuple

import pandas as pd
import requests
from proofreading_cli.config import Config
from proofreading_cli.constants import (
    INFERENCE_SERVER_API_KEY,
    MODEL_VERSION_1,
    MODEL_VERSION_2,
)


class InferenceServerClient:
    def __init__(self, config: Config):
        self.model_1_endpoint = config.proofreading.inference.endpoint.model_1
        self.model_2_endpoint = config.proofreading.inference.endpoint.model_2
        self.api_key = os.getenv(INFERENCE_SERVER_API_KEY)
        self.headers = {
            "Content-Type": "application/json",
            "API-KEY": self.api_key,
        }
        self.timeout = config.proofreading.api.timeout

    def apply_inference(
        self, dataset: pd.DataFrame, model_types: Tuple[str]
    ) -> pd.DataFrame:
        if MODEL_VERSION_1 in model_types:
            responses = dataset.apply(
                lambda row: self.fetch_model_response(row, self.model_1_endpoint),
                axis=1,
            )
            dataset[f"{MODEL_VERSION_1}_label"] = responses.apply(
                lambda res: res["label"]
            )
            dataset[f"{MODEL_VERSION_1}_probability"] = responses.apply(
                lambda res: res["probability"]
            )

        if MODEL_VERSION_2 in model_types:
            responses = dataset.apply(
                lambda row: self.fetch_model_response(row, self.model_2_endpoint),
                axis=1,
            )
            dataset[f"{MODEL_VERSION_2}_label"] = responses.apply(
                lambda res: res["label"]
            )
            dataset[f"{MODEL_VERSION_2}_probability"] = responses.apply(
                lambda res: res["probability"]
            )

        return dataset

    def get_exact_model_version(self, model: str) -> str:
        empty_data = {
            "body": "empty",
            "headline": "empty",
            "lectorate_search_term": "empty",
            "search_dimension_name": "empty",
        }

        response = self.fetch_model_response(empty_data, endpoint=self.model_2_endpoint)
        return response["model_version"]

    def fetch_model_response(self, row: pd.Series, endpoint: str) -> Any:
        data = {
            "body": row["body"],
            "headline": row["headline"],
            "search_term": row["lectorate_search_term"],
            "search_dimension": row["search_dimension_name"],
        }
        response = requests.post(endpoint, headers=self.headers, data=json.dumps(data))
        return response.json()
