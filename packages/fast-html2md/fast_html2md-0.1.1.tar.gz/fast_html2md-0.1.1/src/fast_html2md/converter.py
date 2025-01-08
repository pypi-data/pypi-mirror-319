import tiktoken
from typing import Optional
from .cleaners import HTMLCleanerPipeline
from .models import MODEL_INFO
from .exceptions import ConversionError


class HTMLToMarkdown:
    """Main converter class for HTML to Markdown conversion."""

    def __init__(self, config: Optional[dict] = None):
        """Initialize the converter with optional configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self._init_config(config)
        self._init_cleaner()

    def _init_config(self, config: Optional[dict]) -> None:
        """Initialize configuration settings.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.model_info = self.config.get('model_info', MODEL_INFO)

    def _init_cleaner(self) -> None:
        """Initialize the HTML cleaner pipeline with current settings."""
        self.cleaner = HTMLCleanerPipeline(
            model=self.model_info.name,
            price_per_million_tokens=self.model_info.price_per_million_tokens,
            extract_body=True,
            remove_attributes=True,
            replace_classes=True,
            replace_ids=True,
            minify=True,
            trim_a_tags=True,
            convert_markdown=True,
        )

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the text.
        
        Args:
            text: Input text to count tokens for
            
        Returns:
            Number of tokens in the text
        """
        encoding = tiktoken.encoding_for_model(self.model_info.name)
        return len(encoding.encode(text))

    def compute_cost(self, token_count: int) -> float:
        """Compute the cost for the given number of tokens.
        
        Args:
            token_count: Number of tokens to compute cost for
            
        Returns:
            Computed cost in currency units
        """
        return (token_count / 1_000_000) * self.model_info.price_per_million_tokens

    def convert(self, html: str) -> str:
        """Convert HTML string to Markdown.

        Args:
            html: Input HTML string

        Returns:
            Converted Markdown string

        Raises:
            ConversionError: If conversion fails
        """
        try:
            result = self.cleaner.clean(html)
            return result
        except Exception as e:
            raise ConversionError(f"Failed to convert HTML: {str(e)}")
