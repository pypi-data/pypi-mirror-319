from pathlib import Path

import polars as pl

import blackfish as bf


class ORCA:
    def __init__(self, output_file: Path):
        self.output_file = output_file

    @property
    def ir_spectrum(self) -> pl.DataFrame:
        return bf.ir_spectrum(self.output_file)

    @property
    def nacme(self) -> pl.DataFrame:
        return bf.nacme(self.output_file)

    @property
    def roots(self) -> pl.DataFrame:
        return bf.roots(self.output_file)

    @property
    def soc_absorption_spectrum(self) -> pl.DataFrame:
        return bf.soc_absorption_spectrum(self.output_file)

    @property
    def soc_states(self) -> pl.DataFrame:
        return bf.soc_states(self.output_file)

    @property
    def soc_absorption_spectrum_chart(self) -> None:
        return bf.soc_absorption_spectrum_chart(self.soc_absorption_spectrum)
