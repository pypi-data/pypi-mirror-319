"""Token-based chunking."""

from typing import Any, Generator, List, Tuple, Union

from tqdm import trange

from chonkie.types import Chunk

from .base import BaseChunker


class TokenChunker(BaseChunker):
    """Chunker that splits text into chunks of a specified token size.

    Args:
        tokenizer: The tokenizer instance to use for encoding/decoding
        chunk_size: Maximum number of tokens per chunk
        chunk_overlap: Number of tokens to overlap between chunks

    """

    def __init__(
        self,
        tokenizer: Union[str, Any] = "gpt2",
        chunk_size: int = 512,
        chunk_overlap: Union[int, float] = 128,
    ) -> None:
        """Initialize the TokenChunker with configuration parameters.

        Args:
            tokenizer: The tokenizer instance to use for encoding/decoding
            chunk_size: Maximum number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks

        Raises:
            ValueError: If chunk_size <= 0 or chunk_overlap >= chunk_size

        """
        super().__init__(tokenizer)
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if isinstance(chunk_overlap, int) and chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        if isinstance(chunk_overlap, float) and chunk_overlap >= 1:
            raise ValueError("chunk_overlap must be less than 1")

        self.chunk_size = chunk_size
        self.chunk_overlap = (
            chunk_overlap
            if isinstance(chunk_overlap, int)
            else int(chunk_overlap * chunk_size)
        )

        self._use_multiprocessing = False
    
    def _create_chunks(
        self,
        chunk_texts: List[str],
        token_groups: List[List[int]],
        token_counts: List[int]
    ) -> List[Chunk]:
        """Create chunks from a list of texts."""
        # Find the overlap lengths for index calculation
        if self.chunk_overlap > 0:
            # we get the overlap texts, that gives you the start_index for the next chunk
            # if the token group is smaller than the overlap, we just use the whole token group
            overlap_texts = self._decode_batch([token_group[-self.chunk_overlap:] 
                                                    if (len(token_group) > self.chunk_overlap)
                                                    else token_group
                                                    for token_group in token_groups])
            overlap_lengths = [len(overlap_text) for overlap_text in overlap_texts]
        else:
            overlap_lengths = [0] * len(token_groups)
        
        # Create the chunks
        chunks = []
        current_index = 0
        for chunk_text, overlap_length, token_count in zip(chunk_texts, overlap_lengths, token_counts):
            start_index = current_index
            end_index = start_index + len(chunk_text)
            chunks.append(
                Chunk(
                    text=chunk_text,
                    start_index=start_index,
                    end_index=end_index,
                    token_count=token_count,
                )
            )
            current_index = end_index - overlap_length
        
        return chunks
    
    def _token_group_generator(self, tokens: List[int]) -> Generator[List[int], None, None]:
        """Generate chunks from a list of tokens."""
        for start in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            end = min(start + self.chunk_size, len(tokens))
            yield tokens[start:end]
            if end == len(tokens):
                break

    def chunk(self, text: str) -> List[Chunk]:
        """Split text into overlapping chunks of specified token size.

        Args:
            text: Input text to be chunked

        Returns:
            List of Chunk objects containing the chunked text and metadata

        """
        if not text.strip():
            return []

        # Encode full text
        text_tokens = self._encode(text)

        # Calculate token groups and counts
        token_groups = list(self._token_group_generator(text_tokens))
        token_counts = [len(toks) for toks in token_groups]

        # decode the token groups into the chunk texts
        chunk_texts = self._decode_batch(token_groups) 

        # Create the chunks from the token groups and token counts
        chunks = self._create_chunks(chunk_texts, token_groups, token_counts)

        return chunks

    def _process_batch(self,
                       chunks: List[Tuple[List[int], int, int]],
                       full_text: str) -> List[Chunk]:
        """Process a batch of chunks."""
        token_lists = [tokens for tokens, _, _ in chunks]
        texts = self._decode_batch(token_lists)

        index_pairs = []
        current_index = 0
        for text in texts:
            start_index = full_text.find(text, current_index)
            end_index = start_index + len(text)
            index_pairs.append((start_index, end_index))
            current_index = end_index
            
        return [
            Chunk(text=text, start_index=start, end_index=end, token_count=len(tokens))
            for text, (start, end), tokens in zip(texts, index_pairs, token_lists)
        ]

    def _process_text_batch(self, texts: List[str]) -> List[List[Chunk]]:
        """Process a batch of texts."""
        # encode the texts into tokens in a batch
        tokens_list = self._encode_batch(texts)
        result = []

        for tokens in tokens_list:
            if not tokens:
                result.append([])
                continue

            # get the token groups
            token_groups = list(self._token_group_generator(tokens))
            
            # get the token counts
            token_counts = [len(token_group) for token_group in token_groups]

            # decode the token groups into the chunk texts
            chunk_texts = self._decode_batch(token_groups)

            # create the chunks from the token groups and token counts
            chunks = self._create_chunks(chunk_texts, token_groups, token_counts)
            result.append(chunks)

        return result

    def chunk_batch(
        self,
        texts: List[str],
        batch_size: int = 1,
        show_progress_bar: bool = True
    ) -> List[List[Chunk]]:
        """Split a batch of texts into their respective chunks.

        Args:
            texts: List of input texts to be chunked
            batch_size: Number of texts to process in a single batch
            show_progress_bar: Whether to show a progress bar

        Returns:
            List of lists of Chunk objects containing the chunked text and metadata

        """
        chunks = []
        for i in trange(0,
                        len(texts),
                        batch_size,
                        desc="🦛",
                        disable=not show_progress_bar, 
                        unit="batch",
                        bar_format="{desc} ch{bar:20}nk {percentage:3.0f}% • {n_fmt}/{total_fmt} batches chunked [{elapsed}<{remaining}, {rate_fmt}] 🌱",
                        ascii=' o'):
            batch_texts = texts[i : min(i + batch_size, len(texts))]
            chunks.extend(self._process_text_batch(batch_texts))
        return chunks
    
    def __call__(self,
                text: Union[str, List[str]],
                batch_size: int = 1,
                show_progress_bar: bool = True) -> Union[List[Chunk], List[List[Chunk]]]:
        """Make the TokenChunker callable directly.
        
        Args:
            text: Input text or list of texts to be chunked
            batch_size: Number of texts to process in a single batch
            show_progress_bar: Whether to show a progress bar (for batch chunking)
        
        Returns:
            List of Chunk objects or list of lists of Chunk

        """
        if isinstance(text, str):
            return self.chunk(text)
        elif isinstance(text, list) and isinstance(text[0], str):
            return self.chunk_batch(text, batch_size, show_progress_bar)
        else:
            raise ValueError("Invalid input type. Expected a string or a list of strings.")

    def __repr__(self) -> str:
        """Return a string representation of the TokenChunker."""
        return (
            f"TokenChunker(tokenizer={self.tokenizer}, "
            f"chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap})"
        )
