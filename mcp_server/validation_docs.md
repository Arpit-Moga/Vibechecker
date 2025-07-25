# validation.py Documentation

## Purpose
Provides strict output validation and serialization for all agent workflows using pydantic models. Ensures all outputs conform to schemas, with robust error handling and edge case management.

## API

### OutputValidator

- `validate_output(data: dict, model: Type[BaseModel]) -> BaseModel`
  - Validates `data` against the provided pydantic model.
  - Returns validated model instance or raises `RuntimeError` with detailed error context.

- `validate_all_agents_output(data: dict) -> AllAgentOutputs`
  - Validates data against the `AllAgentOutputs` model.
  - Returns validated model or raises `RuntimeError`.

- `serialize(model: BaseModel) -> str`
  - Serializes any pydantic model to JSON string.

- `to_dict(model: BaseModel) -> dict`
  - Serializes any pydantic model to dict.

## Error Handling
- All validation errors are reported with field, type, and context.
- Handles missing fields, type mismatches, extra fields, and custom validator errors.

## Usage Example
```python
from mcp_server.models import DocumentationOutput
from mcp_server.validation import OutputValidator

raw_data = {"files": {"README.md": "...", ...}}
validated = OutputValidator.validate_output(raw_data, DocumentationOutput)
json_str = OutputValidator.serialize(validated)
dict_obj = OutputValidator.to_dict(validated)
```

## Integration
- Use in orchestration, endpoint, and workflow code to ensure all agent outputs are strictly validated before further processing or storage.
- Recommended to catch `RuntimeError` and log/report errors for debugging and user feedback.

## See Also
- [models.py](./models.py) for schema definitions
- [validation_tests.py](./validation_tests.py) for test coverage
