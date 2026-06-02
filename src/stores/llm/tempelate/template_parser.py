from importlib import import_module
from string import Template


class TemplateParser:

    def __init__(
        self,
        language: str = "en"
    ):

        self.language = language


    def set_language(
        self,
        language: str
    ):

        self.language = language


    def get(
        self,
        group: str,
        key: str,
        variables: dict | None = None
    ):

        module = import_module(

            f"stores.llm.tempelate.locales."
            f"{self.language}.{group}"
        )

        template = getattr(
            module,
            key
        )

        if variables:

            return Template(
                template
            ).safe_substitute(
                variables
            )

        return template