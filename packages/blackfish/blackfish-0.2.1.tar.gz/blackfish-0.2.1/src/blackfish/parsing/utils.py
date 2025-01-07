from typing import List

from blackfish.parsing.exceptions import ParsingError


def find_table_start(lines: List[str], header: str, offset: int) -> int:
    """
    Find the starting index of a table in ORCA output files.

    Args:
        lines: List of strings containing the file content
        header: The header text to search for
        offset: Number of lines to skip after the header (default=5)

    Returns:
        int: The index where the table data starts

    Raises:
        ParsingError: If the header is not found in the file
    """
    try:
        table_start_idx = next(
            i for i, line in enumerate(lines) if header in line.strip()
        )
    except StopIteration:
        raise ParsingError(f"Could not find '{header}'")

    return table_start_idx + offset
