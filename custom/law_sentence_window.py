import json
from typing import Any, Callable, List, Optional, Sequence
from bisect import bisect_right
from pathlib import Path

from llama_index.core.bridge.pydantic import Field
from llama_index.core.callbacks import CallbackManager
from llama_index.core.node_parser import NodeParser
from llama_index.core.node_parser.node_utils import build_nodes_from_splits
from llama_index.core.node_parser.text.utils import split_by_sentence_tokenizer
from llama_index.core.schema import BaseNode, MetadataMode
from llama_index.core import Document
from llama_index.core.utils import get_tqdm_iterable

DEFAULT_WINDOW_SIZE = 3
DEFAULT_WINDOW_METADATA_KEY = "window"
DEFAULT_OG_TEXT_METADATA_KEY = "original_text"

class LawSentenceWindowNodeParser(NodeParser):
    sentence_splitter: Callable[[str], List[str]] = Field(
        default_factory=split_by_sentence_tokenizer,
        description="The text splitter to use when splitting documents.",
        exclude=True,
    )
    window_size: int = Field(
        default=DEFAULT_WINDOW_SIZE,
        description="The number of sentences on each side of a sentence to capture.",
        gt=0,
    )
    window_metadata_key: str = Field(
        default=DEFAULT_WINDOW_METADATA_KEY,
        description="The metadata key to store the sentence window under.",
    )
    original_text_metadata_key: str = Field(
        default=DEFAULT_OG_TEXT_METADATA_KEY,
        description="The metadata key to store the original sentence in.",
    )

    @classmethod
    def class_name(cls) -> str:
        return "LawSentenceWindowNodeParser"

    @classmethod
    def load_mapping(cls, path: str) -> dict:
        """Load the mapping from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def book_name(cls, path: str) -> str:
        """Get the book name from the mapping."""
        # Load the mapping from the JSON file
        mapping_path = Path(__file__).parent / "mapping.json"
        _mapping = cls.load_mapping(mapping_path)

        # Find the book name based on the file path
        for name in _mapping:
            if name in path:
                return _mapping[name]
        return "未名"

    @classmethod
    def from_defaults(
            cls,
            sentence_splitter: Optional[Callable[[str], List[str]]] = None,
            window_size: int = DEFAULT_WINDOW_SIZE,
            window_metadata_key: str = DEFAULT_WINDOW_METADATA_KEY,
            original_text_metadata_key: str = DEFAULT_OG_TEXT_METADATA_KEY,
            include_metadata: bool = True,
            include_prev_next_rel: bool = True,
            callback_manager: Optional[CallbackManager] = None,
    ) -> "LawSentenceWindowNodeParser":
        callback_manager = callback_manager or CallbackManager([])

        sentence_splitter = sentence_splitter or split_by_sentence_tokenizer()

        return cls(
            sentence_splitter=sentence_splitter,
            window_size=window_size,
            window_metadata_key=window_metadata_key,
            original_text_metadata_key=original_text_metadata_key,
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            callback_manager=callback_manager,
        )

    def _parse_nodes(
            self,
            nodes: Sequence[BaseNode],
            show_progress: bool = False,
            **kwargs: Any,
    ) -> List[BaseNode]:
        """Parse document into nodes."""
        all_nodes: List[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            self.sentence_splitter(node.get_content(metadata_mode=MetadataMode.NONE))
            nodes = self.build_window_nodes_from_documents([node])
            all_nodes.extend(nodes)

        return all_nodes

    def analyze_titles(self, text):
        lines = text.split('\n')
        titles = []
        for i, line in enumerate(lines):
            if len(line) > 0 and line[0] != '\n' and line[0] != '\u3000' and line[0] != ' ':
                if '纪' not in line and '传' not in line and '法' not in line:
                    continue
                titles.append([line.strip(), i])
        return TitleLocalizer(titles, len(lines))

    def build_window_nodes_from_documents(
            self, documents: Sequence[Document]
    ) -> List[BaseNode]:
        """Build window nodes from documents."""
        all_nodes: List[BaseNode] = []
        for doc in documents:
            text = doc.text
            title_localizer = self.analyze_titles(text)
            lines = text.split('\n')
            nodes = []
            book_name = LawSentenceWindowNodeParser.book_name(doc.metadata['file_name'])
            for i, line in enumerate(lines):
                if len(line) == 0:
                    continue
                text_splits = self.sentence_splitter(line)
                line_nodes = build_nodes_from_splits(
                    text_splits,
                    doc,
                    id_func=self.id_func,
                )
                title = title_localizer.get_title_line(i)
                if title == None:
                    continue
                for line_node in line_nodes:
                    line_node.metadata["出处"] = f"《{book_name}·{title[0]}》"
                nodes.extend(line_nodes)
            for i, node in enumerate(nodes):
                window_nodes = nodes[
                               max(0, i - self.window_size) : min(i + self.window_size, len(nodes))
                               ]

                node.metadata[self.window_metadata_key] = " ".join(
                    [n.text for n in window_nodes]
                )
                node.metadata[self.original_text_metadata_key] = node.text

                # exclude window metadata from embed and llm
                node.excluded_embed_metadata_keys.extend(
                    [self.window_metadata_key, self.original_text_metadata_key, 'title', 'file_path', '出处', 'file_name', 'filename', 'extension']
                )
                node.excluded_llm_metadata_keys.extend(
                    [self.window_metadata_key, self.original_text_metadata_key, 'file_path', 'file_name', 'filename', 'extension']
                )

                all_nodes.append(node)
        return all_nodes

class TitleLocalizer():
    def __init__(self, titles, total_lines):
        self._titles = titles
        self._total_lines = total_lines

    def get_title_line(self, line_id):
        indices = [title[1] for title in self._titles]
        index = bisect_right(indices, line_id)
        if index - 1 < 0:
            return None
        return self._titles[index-1]
        
   
