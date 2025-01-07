# PydanticAI GenAI Hub

A Python library providing Pydantic-based model implementations for various LLM providers.

## Installation

You can install the package with pip:

```bash
pip install pydanticai-genai-hub
```

To install with specific provider support:

```bash
# For Anthropic support
pip install "pydanticai-genai-hub[anthropic]"

# For OpenAI support
pip install "pydanticai-genai-hub[openai]"

# For all providers
pip install "pydanticai-genai-hub[all]"
```

## Usage

### Anthropic Model

```python
from pydanticai_genai_hub.anthropic import AnthropicModel

model = AnthropicModel(
    model_name="claude-3",
    deployment_id="your-deployment-id",  # optional
    config_name="your-config-name",      # optional
)
```

### OpenAI Model

```python
from pydanticai_genai_hub.openai import OpenAIModel

model = OpenAIModel(
    model_name="gpt-4",
    api_key="your-api-key",      # optional, can use OPENAI_API_KEY env var
    base_url="your-base-url",    # optional
)
```

## License

MIT License
