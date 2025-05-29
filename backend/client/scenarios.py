from typing import Optional
import json

from pydantic import BaseModel, ValidationError, Field
from pydantic.type_adapter import TypeAdapter

class Scenario:
    def __init__(self, name: str, prompt: str):
        self.name = name
        self.prompt = prompt

    def validate(self, raw_output: str) -> bool:
        try:
            data = json.loads(raw_output)
            adapter = TypeAdapter(self.validator_model)
            adapter.validate_python(data)
            return True
        except (ValidationError, json.JSONDecodeError) as e:
            print(f"Validation error for scenario '{self.name}': {e}")
            return False

class ScenarioResult(BaseModel):
    success: bool = Field(..., description="Whether the scenario was successfully fulfilled")
    reason: Optional[str] = Field(None, description="Reason for failure or confirmation of success")

scenarios_list = [
    Scenario(
        name="Create Item",
        prompt="Create a new item named 'Test Item' with description 'This is a test item.'",
    ),
    Scenario(
        name="List Items",
        prompt="List all items in the inventory.",
    ),
    Scenario(
        name="Update Item",
        prompt="Update the item with ID 1 to have the name 'Updated Item' and description 'Updated description.'",
    ),
    Scenario(
        name="Get Item",
        prompt="Retrieve the item with ID 1.",
    ),
    Scenario(
        name="Delete Item",
        prompt="Delete the item with ID 1.",
    ),
]
