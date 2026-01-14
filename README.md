
# sortGPT

Small FastAPI service that uses modern technology of Generative AI to sort data. it doesn't require any specification how to sort these items, the algorithm will determine it on its own.

DISCLAIMER: since program uses very advanced method, generating result might take some time

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # on macOS/Linux
pip install -r requirements.txt
```

The model used is `microsoft/phi-2` via `transformers` and `torch`.

## Running the API

From the project root (`sortGPT/`):

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000` by default.

## Sorting endpoint

- **Path:** `POST /sort`
- **Request body (JSON):**

	```json
	{
		"items": ["a", "d", "c"]
	}
	```

- **Response (JSON):**

	```json
	{
		"input": ["a", "d", "c"],
		"model_output": ["a", "c", "d"]
	}
	```

`model_output` is always a proper JSON array.

## Debugging prompt check iterations

The function `sort_items_with_model` in `logic/sorter.py` calls the model up to
10 times to verify that the output is a clean JSON array.

To see how many times the prompt check loop fired, you can log the count on the server side. For example:


