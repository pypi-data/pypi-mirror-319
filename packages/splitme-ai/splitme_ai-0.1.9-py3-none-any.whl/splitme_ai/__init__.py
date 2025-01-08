from splitme_ai.config import Config as Config
from splitme_ai.core import MarkdownSplitter as MarkdownSplitter
from splitme_ai.errors import FileOperationError as FileOperationError
from splitme_ai.errors import ParseError as ParseError
from splitme_ai.errors import SplitmeAIBaseError
from splitme_ai.utils.file_handler import FileHandler

# from splitme_ai.utils.version import get_version

__version__ = "0.1.8"  # get_version()

__all__: list[str] = [
    "Config",
    "FileHandler",
    "FileOperationError",
    "MarkdownSplitter",
    "ParseError",
    "SplitmeAIBaseError",
    # "get_version",
]
