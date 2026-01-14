from fastapi import FastAPI
from pydantic import BaseModel

from logic.sorter import sort_items_with_model


app = FastAPI(title="sortGPT API")


class SortRequest(BaseModel):
    items: list[str]
    max_tokens: int | None = None


@app.post("/sort")
def sort_items(req: SortRequest):
    sorted_items = sort_items_with_model(req.items, max_tokens=req.max_tokens)
    return {
        "input": req.items,
        "model_output": sorted_items,
    }
