import altair as alt
import polars as pl

from blackfish.charts.gaussian_broadening import apply_gaussian_filter


def soc_absorption_spectrum_chart(df: pl.DataFrame, fwhm: int = 2000) -> alt.Chart:
    bar = (
        alt.Chart(df)
        .mark_bar(opacity=0.5)
        .encode(
            x=alt.X("energy_cm:Q", title="Energy [1/cm]"),
            y=alt.Y("rel_intensity:Q", title="Rel. Intensity"),
            color=alt.value("red"),
            tooltip=["energy_cm", "rel_intensity"],
        )
    )

    simulated_df = apply_gaussian_filter(df, "energy_cm", "rel_intensity", fwhm, 10)

    line = (
        alt.Chart(simulated_df)
        .mark_line()
        .encode(x="energy_cm:Q", y="rel_intensity:Q", color=alt.value("black"))
    )
    chart = bar + line

    return chart
