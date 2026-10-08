from openai import NotFoundError, OpenAI

from simple_rag.config import get_settings


settings = get_settings()

def connect_to_openai() -> OpenAI:
    
    return OpenAI(api_key=settings.GROQ_API_KEY , base_url=settings.GROQ_BASE_URL)


def answer(context: str, question: str, max_tokens: int = 250) -> str:
    
    if not settings.GROQ_API_KEY:
        raise ValueError("Set GROQ_API_KEY in .env before asking questions.")

    client = connect_to_openai()

    prompt = (
        "Context:\n" + context + "\n\n"
        "Question: " + question + "\n"
        "Answer using only the context above. "
        "If the context does not contain the answer, say so clearly."
    )

    if not settings.PREFERRED_MODELS:
        raise ValueError("Add at least one model ID to PREFERRED_MODELS in .env.")

    response = None
    for model in settings.PREFERRED_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            break
        except NotFoundError:
            if model == settings.PREFERRED_MODELS[-1]:
                raise

    if response is None:
        raise RuntimeError("No configured model could answer the question.")

    text = response.choices[0].message.content

    if not text or not text.strip():
        reason = response.choices[0].finish_reason
        return f"[EMPTY ANSWER - finish_reason={reason}, try a larger max_tokens]"
    return text.strip()