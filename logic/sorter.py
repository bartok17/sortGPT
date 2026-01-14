import ast
import json
from typing import List, Any

from model.model import run


def _extract_list_literal(text: str) -> str:
	"""Extract the first bracketed list literal from model output.

	"""
	text = text.strip()
	start = text.find("[")
	end = text.rfind("]")
	if start != -1:
		if end != -1 and end > start:
			return text[start : end + 1]
		# No closing bracket
		return text[start:]
	return text


def parse_model_output_to_list(output: str) -> List[str]:
	"""Parse the language model output into a Python list of strings.

	Tries JSON, then Python literal syntax, and finally falls back to
	splitting non-empty lines.
	"""

	candidate = _extract_list_literal(output)

	# JSON parsing
	try:
		value: Any = json.loads(candidate)
		if isinstance(value, list):
			return [str(item) for item in value]
	except Exception:
		pass

	# Python list literal parsing
	try:
		value = ast.literal_eval(candidate)
		if isinstance(value, list):
			return [str(item) for item in value]
	except Exception:
		pass

	# Fallback: split by lines and commas, then clean tokens
	if "\n" in candidate:
		raw_parts = [p.strip() for p in candidate.splitlines() if p.strip()]
	else:
		raw_parts = [p.strip() for p in candidate.split(",") if p.strip()]

	cleaned: List[str] = []
	for part in raw_parts:
		# Remove common surrounding characters
		item = part.strip().lstrip("A:").strip()
		item = item.strip("[] ,\"'\t")
		if not item:
			continue
		cleaned.append(item)

	return cleaned


def sort_items_with_model(items: List[str]) -> List[str]:
    """Use the language model to sort the given items.

    Returns a list of strings (suitable for JSON encoding).
    """

    prompt = (
        "Sort the following items using best method possible for the situation, try to prioritize alphabetical order. Respond with ONLY a JSON array "
        "of the sorted items, for example: [\"a\", \"b\", \"c\"]. "
        "Do not include any prefixes (like 'A:'), keys, or extra text. "
        f"Items: {items}"
    )

    raw_output = run(prompt)
    
    attempts = 0
    

    for _ in range(10):
		
        attempts += 1

        prompt_check = (
            "respond with False if the input in <> is ONLY JSON array "
            "otherwise respond with True. dont return anything outside True or False. "
            f"here is the text to check:<{raw_output}>"
        )
        check = run(prompt_check)
        is_invalid = check.strip().lower() == "true"
        if not is_invalid:
            break
        raw_output = run(prompt)

    print(f"prompt check fired {attempts} time(s)")
    print(f"before parsing: {raw_output}")


    return parse_model_output_to_list(raw_output)

