# Portia SDK Python


## Usage

### Installation

```bash
pip install portia-sdk-python 
```


### Simple Usage

```python
from portia.runner import Runner, RunnerConfig

runner = Runner(config=RunnerConfig(portia_api_key='123'))
runner.run_query("Add 1 and 2")
```


### With Custom Local Tools and Disk Storage

```python
from portia.runner import Runner, RunnerConfig, StorageClass
from portia.tool import Tool
from portia.tool_registry import InMemoryToolRegistry

# Create a local tool
class AdditionTool(Tool):
    id: str = "addition_tool"
    name: str = "Addition Tool"
    description: str = "Takes two numbers and adds them together"

    def run(self, a: int, b: int) -> int:
        return a + b


# Create the ToolRegistry with the tool
tool_registry = InMemoryToolRegistry.from_local_tools([AdditionTool()])

runner = Runner(config=Config(), tool_registry=tool_registry)
runner.run_query("Add 1 and 2")
```

### Hybrid Approach

Multiple registries can be combined to give the power of Portia Cloud with the customization of local tools:

```python
from pydantic import BaseModel, Field, SecretStr

from portia.config import StorageClass, default_config
from portia.runner import Runner
from portia.tool import Tool
from portia.tool_registry import InMemoryToolRegistry, PortiaToolRegistry
from portia.workflow import WorkflowState
from portia.clarification import InputClarification


class AdditionToolSchema(BaseModel):
    """Input for AdditionToolSchema."""

    a: float = Field(..., description="The first number to add")
    b: float = Field(..., description="The second number to add")


class AdditionTool(Tool):
    """Adds two numbers."""

    id: str = "add_tool"
    name: str = "Add Tool"
    description: str = "Takes two numbers and adds them together"
    args_schema: type[BaseModel] = AdditionToolSchema
    output_schema: tuple[str, str] = ("int", "int: The value of the addition")

    def run(self, a: float, b: float) -> float | InputClarification:
        """Add the numbers."""
        return a + b


# Create the ToolRegistry with the tool

config = default_config()

local_registry = InMemoryToolRegistry.from_local_tools([AdditionTool()]) 
remote_registry = PortiaToolRegistry(
    config=config,
)
registry = local_registry + remote_registry

runner = Runner(
    config,
    tool_registry=registry,
)

runner.run_query("Add 1 and 2")
```


## Tests

We write two types of tests:
- Unit tests should mock out the LLM providers, and aim to give quick feedback. 
- Integration tests actually call LLM providers, are much slower but test the system works fully.

To run tests:
- Run all tests with `poetry run pytest`.
- Run unit tests with `poetry run pytest tests/unit`.
- Run integration tests with `poetry run pytest tests/integration`.

We utilize [pytest-parallel](https://pypi.org/project/pytest-parallel/) to execute tests in parallel. You can add the `--workers=4` argument to the commands above to run in parallel. If you run into issues running this try setting `export NO_PROXY=true` first.

## Release

Releases are controlled via Github Actions and the version field of the `pyproject.toml`. To release:

1. Create a PR that updates the version field in the `pyproject.toml`.
2. Merge the PR to main.
3. Github Actions will create a new tag and push the new version to PyPi.

## CLI 

To test the CLI locally run 

```bash
pip install -e . 
export OPENAI_API_KEY=$KEY
portia-cli run "add 4 + 8"
```

## Logging

Custom tools can make use of the portia logging:

```python
from portia.logging import logger

class AdditionTool(Tool):
    """Adds two numbers."""
    def run(self, a: float, b: float) -> float | InputClarification:
        """Add the numbers."""
        logger.debug(f"Adding {a} and {b}")
        return a + b

```

The logging implementation itself can also be overridden by any logger that fulfils the LoggerInterface.

For example to use the built in python logger:

```python
import logging
from portia.logging import logger_manager

logger = logging.getLogger(__name__)

logger_manager.set_logger(logger)
```
