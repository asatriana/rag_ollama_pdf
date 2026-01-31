import os


def get_embeddings():
    """
    Factory embeddings.
    Provider dikontrol via environment variable:

      EMBEDDING_PROVIDER = ollama | hf | openai

    Default: ollama (local, ringan, stabil)
    """

    provider = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()

    # -------------------------------------------------
    # 1) OLLAMA (LOCAL-FIRST, RECOMMENDED DEFAULT)
    # -------------------------------------------------
    if provider == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError as e:
            raise ImportError(
                "langchain-ollama belum terinstall. "
                "Install dengan: pip install langchain-ollama"
            ) from e

        model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
        return OllamaEmbeddings(model=model)

    # -------------------------------------------------
    # 2) HUGGINGFACE (LOCAL / GPU / ACADEMIC)
    # -------------------------------------------------
    elif provider == "hf":
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError as e:
            raise ImportError(
                "langchain-huggingface belum terinstall. "
                "Install dengan: pip install langchain-huggingface sentence-transformers"
            ) from e

        model = os.getenv(
            "HF_EMBED_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        return HuggingFaceEmbeddings(model_name=model)

    # -------------------------------------------------
    # 3) OPENAI (CLOUD / PRODUCTION)
    # -------------------------------------------------
    elif provider == "openai":
        try:
            from langchain_openai import OpenAIEmbeddings
        except ImportError as e:
            raise ImportError(
                "langchain-openai belum terinstall. "
                "Install dengan: pip install langchain-openai"
            ) from e

        model = os.getenv(
            "OPENAI_EMBED_MODEL",
            "text-embedding-3-large"
        )
        return OpenAIEmbeddings(model=model)

    # -------------------------------------------------
    # UNKNOWN PROVIDER
    # -------------------------------------------------
    else:
        raise ValueError(
            f"EMBEDDING_PROVIDER tidak dikenali: '{provider}'.\n"
            "Gunakan salah satu: ollama | hf | openai"
        )
