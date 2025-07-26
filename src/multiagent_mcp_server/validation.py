"""
Output serialization and validation logic for agent workflows
Strictly uses pydantic models and handles validation errors/edge cases
"""
from typing import Type
from multiagent_mcp_server.models import AllAgentOutputs, DocumentationOutput, AgentReport, IssueOutput
from pydantic import ValidationError, BaseModel

class OutputValidator:
    @staticmethod
    def validate_output(data: dict, model: Type[BaseModel]) -> BaseModel:
        """
        Validate data against the provided pydantic model.
        Returns validated model instance or raises RuntimeError with details.
        """
        try:
            validated = model(**data)
            return validated
        except ValidationError as e:
            # Detailed error reporting
            error_details = e.errors()
            msg = f"Validation failed for {model.__name__}:\n"
            for err in error_details:
                loc = '.'.join(str(x) for x in err['loc'])
                msg += f"- Field: {loc}, Error: {err['msg']}, Type: {err['type']}\n"
            raise RuntimeError(msg)

    @staticmethod
    def validate_all_agents_output(data: dict) -> AllAgentOutputs:
        """
        Validate data against AllAgentOutputs model.
        """
        return OutputValidator.validate_output(data, AllAgentOutputs)

    @staticmethod
    def serialize(model: BaseModel) -> str:
        """
        Serialize any pydantic model to JSON.
        """
        return model.model_dump_json(indent=2)

    @staticmethod
    def to_dict(model: BaseModel) -> dict:
        """
        Serialize any pydantic model to dict.
        """
        return model.model_dump()

# Usage example (for orchestration/workflow):
# validated = OutputValidator.validate_output(raw_data, DocumentationOutput)
# serialized = OutputValidator.serialize(validated)
# dict_obj = OutputValidator.to_dict(validated)
