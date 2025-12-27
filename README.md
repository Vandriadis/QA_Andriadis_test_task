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

Run UI tests:
```bash
# Run with Chrome (default)
pytest tests/ui/ --browser=chrome

# Run with Firefox
pytest tests/ui/ --browser=firefox

# Run in headless mode
pytest tests/ui/ --browser=chrome --headless
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
  ui/          - UI automation (Page Object Model)
    base_page.py - Base page class
    pages/       - Page classes
    utils/       - Browser factory, screenshots
tests/
  api/         - API tests
  ui/          - UI tests
```

## Features

- Strict contract validation with Pydantic
- Type-safe API responses
- Positive and negative test scenarios
- Contract violation detection
- UI automation with Page Object Model (POM)
- Multi-browser support (Chrome, Firefox)
- Automatic screenshots on test failure

