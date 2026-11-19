"""Console table printing utility."""

from typing import Any, Sequence


def print_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    """Print tabular data with aligned columns, separator, and record count."""
    if not headers:
        print("No columns to display.\n")
        return

    string_rows = [[str(cell) if cell is not None else "" for cell in row] for row in rows]
    col_widths = [len(str(h)) for h in headers]

    for row in string_rows:
        for idx, cell in enumerate(row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(cell))

    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

    print()
    print(header_line)
    print(separator)
    if string_rows:
        for row in string_rows:
            padded_row = row + [""] * (len(headers) - len(row))
            print(" | ".join(padded_row[i].ljust(col_widths[i]) for i in range(len(headers))))
    else:
        print("No records found.")
    print(separator)
    print(f"Total records: {len(rows)}\n")

