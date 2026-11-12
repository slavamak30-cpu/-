import re

def split_text(text, chunk_size=500, overlap=50):
    if not isinstance(text, str):
        raise TypeError("text должен быть строкой")
    if type(chunk_size) is not int or chunk_size <= 0:
        raise ValueError("chunk_size должен быть положительным целым")
    if type(overlap) is not int or not 0 <= overlap < chunk_size:
        raise ValueError("Требуется 0 <= overlap < chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            lower = start + max(chunk_size // 2, overlap + 1)
            tail = text[lower:end]

            # Приоритет: абзац -> предложение -> пробел.
            for pattern in (r"\n\s*\n", r"(?<=[.!?…])\s+", r"\s+"):
                matches = list(re.finditer(pattern, tail))
                if matches:
                    end = lower + matches[-1].end()
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks
