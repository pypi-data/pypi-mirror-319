async def collect_text(async_text_iter) -> tuple[str, int]:
    full_text = ""
    num_completion_tokens = 0
    async for delta in async_text_iter:
        num_completion_tokens += len(delta.output_ids)
        full_text += delta.output_text
    return full_text, num_completion_tokens
