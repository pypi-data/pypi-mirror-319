from pathlib import Path

import polars as pl

from .utils import find_table_start


def nacme(orca_output: Path) -> pl.DataFrame:
    lines = Path(orca_output).read_text().splitlines()

    TABLE_HEADER = "CARTESIAN NON-ADIABATIC COUPLINGS"
    TABLE_HEADER_OFFSET = 5

    table_start_idx = find_table_start(lines, TABLE_HEADER, TABLE_HEADER_OFFSET)

    # Collect table
    rows = []
    for row in lines[table_start_idx:]:
        # Stop on empty line
        if not row.strip():
            break

        rows.append(row.split())

    df = pl.DataFrame(
        rows,
        schema={"id": int, "symbol": str, "_": str, "x": float, "y": float, "z": float},
        orient="row",
    ).drop("_")

    # Compute magnitude
    df = df.with_columns(
        (pl.col("x").abs() + pl.col("y").abs() + pl.col("z").abs()).alias("magnitude")
    )

    return df
