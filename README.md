# Petstore API Test Automation

API test automation project for Petstore Swagger with strict contract validation using Pydantic.

## Requirements

- Python 3.9+
- pip

## Installation

Create and activate virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -e .
```

Optional (for Allure reports):
```bash
pip install -e ".[allure]"
```

## Running Tests

Make sure virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Run all tests:
```bash
pytest
```

Run specific test files:
```bash
pytest tests/api/test_pet_crud_positive.py
pytest tests/api/test_pet_crud_negative.py
pytest tests/api/test_pet_contracts.py
```

Run with Allure (if installed):
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

**Note:** Always use the virtual environment to avoid conflicts with globally installed pytest plugins.

## Project Structure

```
src/
  config/      - Configuration settings
  http/        - HTTP client layer
  api/         - API methods
  contracts/   - Contract validators
  models/      - Pydantic models
  utils/       - Utilities (data factories)
tests/
  api/         - API tests
ui/            - Reserved for future UI tests
```

## Features

- Strict contract validation with Pydantic
- Type-safe API responses
- Positive and negative test scenarios
- Contract violation detection
- Extensible architecture for UI tests

