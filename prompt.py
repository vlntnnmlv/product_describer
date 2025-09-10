# product_describer/prompt.py
def build_batch_prompt(products: list[str], keyword_count: int, description_max_length: int) -> str:
    numbered = "\n".join(f"{i+1}. {p}" for i, p in enumerate(products))
    return f"""
You are a product copywriter. For each product below, generate:
- a short description for each product (<{description_max_length} characters)
- exactly {keyword_count} single-word keywords

Products:
{numbered}

Return JSON array of objects, like:
[
{{"product": "product1", "description": "desc1", "keywords": ["k1","k2","k3",...]}},
...
]
"""
