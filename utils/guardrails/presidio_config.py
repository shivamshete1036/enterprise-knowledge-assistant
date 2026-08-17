from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import (
    NlpEngineProvider,
)


def create_presidio_analyzer() -> AnalyzerEngine:
    """
    Create a Presidio AnalyzerEngine using the lightweight
    spaCy English model already installed locally.
    """

    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": "en",
                "model_name": "en_core_web_sm",
            }
        ],
    }

    provider = NlpEngineProvider(
        nlp_configuration=configuration
    )

    nlp_engine = provider.create_engine()

    return AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages=["en"],
    )