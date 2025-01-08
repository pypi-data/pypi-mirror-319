import json
import urllib.parse
from copy import deepcopy
from typing import List

from pydantic import BaseModel

from tinybird.client import TinyB


class DataFile(BaseModel):
    name: str
    content: str


class DataProject(BaseModel):
    datasources: List[DataFile]
    pipes: List[DataFile]


class TestExpectation(BaseModel):
    name: str
    description: str
    parameters: str


class TestExpectations(BaseModel):
    tests: List[TestExpectation]


class LLM:
    def __init__(
        self,
        user_token: str,
        client: TinyB,
    ):
        self.user_client = deepcopy(client)
        self.user_client.token = user_token

    async def ask(self, prompt: str, system_prompt: str = "", model: str = "o1-mini") -> str:
        """
        Calls the model with the given prompt and returns the response.

        Args:
            prompt (str): The user prompt to send to the model.

        Returns:
            str: The response from the language model.
        """
        messages = []

        if system_prompt:
            messages.append({"role": "user", "content": system_prompt})

        if prompt:
            messages.append({"role": "user", "content": prompt})

        data = {
            "model": model,
            "messages": messages,
        }
        response = await self.user_client._req(
            "/v0/llm",
            method="POST",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return response.get("result", "")

    async def create_project(self, prompt: str) -> DataProject:
        try:
            prompt = (
                prompt
                + "\n#More extra context\n- If you add some array data type remember that the json path should be like this: `json:$.array_field[:]`"
            )
            response = await self.user_client._req(
                "/v0/llm/create",
                method="POST",
                data=f'{{"prompt": {json.dumps(prompt)}}}',
                headers={"Content-Type": "application/json"},
            )

            return DataProject.model_validate(response.get("result", {}))
        except Exception:
            return DataProject(datasources=[], pipes=[])

    async def generate_sql_sample_data(self, schema: str, rows: int = 20, prompt: str = "") -> str:
        response = await self.user_client._req(
            "/v0/llm/mock",
            method="POST",
            data=f'{{"schema": "{urllib.parse.quote(schema)}", "rows": {rows}, "context": "{prompt}"}}',
            headers={"Content-Type": "application/json"},
        )
        result = response.get("result", "")
        return result.replace("elementAt", "arrayElement")

    async def create_tests(self, pipe_content: str, pipe_params: set[str], prompt: str = "") -> TestExpectations:
        response = await self.user_client._req(
            "/v0/llm/create/tests",
            method="POST",
            data=json.dumps({"pipe_content": pipe_content, "pipe_params": list(pipe_params), "prompt": prompt}),
            headers={"Content-Type": "application/json"},
        )
        result = response.get("result", "")
        return TestExpectations.model_validate(result)
