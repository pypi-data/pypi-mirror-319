import shutil
import sys
from typing import Dict, Tuple

import click
import pandas as pd
from proofreading_cli.api_client import ApiClient
from proofreading_cli.common import save
from proofreading_cli.config import Config
from proofreading_cli.constants import (
    EMOJIS,
    GC_API_KEY_ENV,
    INFERENCE_SERVER_API_KEY,
    MODEL_VERSION_1,
    MODEL_VERSION_2,
    RAW_HITS_DATASET_NAME,
)
from proofreading_cli.inference_server_client import InferenceServerClient
from proofreading_cli.paths import SETTINGS_PATH
from proofreading_cli.utils import (
    build_cli_options,
    build_filters,
    exclude_missing_cols,
    format_table,
    is_api_key_missing_from_env,
    is_start_date_after_end_date,
    validate_date,
    wrap_text_in_df,
)
from tabulate import tabulate

config = Config.load(SETTINGS_PATH)
gc_api_client = ApiClient(config)
inference_server_client = InferenceServerClient(config)
pd.set_option("max_colwidth", config.proofreading.cli.max_colwidth)


@click.group()
def cli():
    """CLI group for managing proofreading operations."""
    pass


@click.command()
@click.option("--article-id", type=str, help="Specify the ID of the article.")
@click.option(
    "--subscription-id",
    type=str,
    help="Specify the subscription ID (default provided).",
)
@click.option(
    "--statuses",
    default=["Accepted", "Rejected", "Ignored"],
    type=click.Choice(["Skipped", "Open", "Accepted", "Rejected", "Ignored"]),
    multiple=True,
    help="Specify proofreading status (default: Accepted, Rejected, Ignored).",
)
@click.option(
    "--is-submitted",
    type=bool,
    default=True,
    help="Specify proofreading submission status.",
)
@click.option(
    "--start-date",
    type=str,
    callback=validate_date,
    help="Specify start date for fetching hits. Format: (YYYY-MM-DD).",
    required=True,
)
@click.option(
    "--end-date",
    type=str,
    callback=validate_date,
    help="Specify end date for fetching hits. Format: (YYYY-MM-DD).",
)
@click.option(
    "--file-system",
    type=str,
    default=config.proofreading.data.path,
    help="Specify path to local directory where data should be saved.",
)
@click.option(
    "--inference",
    default=[MODEL_VERSION_1, MODEL_VERSION_2],
    type=click.Choice([MODEL_VERSION_1, MODEL_VERSION_2]),
    multiple=True,
    help="Add inference columns (label, probability, and model_version) to the dataset.",
)
@click.option("--sneak-peek", type=bool, default=True, help="Show dataset preview.")
def hits(
    article_id: str,
    subscription_id: str,
    statuses: Tuple[str],
    is_submitted: bool,
    start_date: str,
    end_date: str,
    file_system: str,
    inference: Tuple[str],
    sneak_peek: bool,
):
    """Fetch and filter hits based on various criteria."""

    if is_api_key_missing_from_env():
        click.echo(
            click.style(
                f"\nExport required environment variables: {GC_API_KEY_ENV} and {INFERENCE_SERVER_API_KEY}.",
                fg="red",
                bold=True,
            )
        )
        sys.exit(1)

    if is_start_date_after_end_date(start_date, end_date):
        click.echo(
            click.style(
                "\nStart date cannot be after the end date.", fg="red", bold=True
            )
        )
        sys.exit(1)

    hit_api_filters: Dict[str, str] = build_filters(
        article_id, subscription_id, statuses, is_submitted, start_date, end_date
    )

    cli_options: Dict[str, str] = build_cli_options(file_system, inference, sneak_peek)

    table_header, table_data = format_table(
        header=["Filter", "Value"], data=hit_api_filters
    )
    hit_api_filters_table = tabulate(
        table_data, headers=table_header, tablefmt="fancy_grid", numalign="center"
    )

    table_header, table_data = format_table(
        header=["CLI Option", "Value"], data=cli_options
    )
    cli_options_table = tabulate(
        table_data, headers=table_header, tablefmt="fancy_grid", numalign="center"
    )

    click.echo(
        tabulate(
            [[hit_api_filters_table, None, None, None, cli_options_table]],
            rowalign="center",
            tablefmt="plain",
        )
    )
    try:
        hits: pd.DataFrame = gc_api_client.get_hits_by_date(params=hit_api_filters)
        click.echo(
            click.style(
                f"\n{EMOJIS['loupe']} Fetched {len(hits)} hits from GC API.",
                fg="bright_blue",
            )
        )

    except Exception as e:
        click.echo(
            click.style(
                f"\nError occurred while fetching hits: {e}\n", fg="red", bold=True
            )
        )
        sys.exit(1)

    if inference:
        model_2_v = inference_server_client.get_exact_model_version(MODEL_VERSION_2)
        click.echo(
            click.style(
                f"{EMOJIS['robot']} Current {MODEL_VERSION_2} version: {model_2_v}.\n",
                fg="bright_blue",
            )
        )
        inference_server_client.apply_inference(hits, inference)

    if sneak_peek:
        if not hits.empty:
            sneak_peak_cols = exclude_missing_cols(
                cols=hits.columns,
                columns_to_select=config.proofreading.cli.sneak_peak_cols,
            )

            max_length = config.proofreading.cli.max_length
            sneak_peak_hits = hits[sneak_peak_cols].head(config.proofreading.cli.show)

            terminal_width = shutil.get_terminal_size().columns

            max_col_width = terminal_width // len(sneak_peak_cols)

            sneak_peak_hits = sneak_peak_hits.map(
                lambda x: x[:max_length] + " ..."
                if isinstance(x, str) and len(x) > max_length
                else x
            )

            sneak_peak_hits = wrap_text_in_df(df=sneak_peak_hits, width=max_col_width)
            table_str = tabulate(
                sneak_peak_hits, headers="keys", tablefmt="fancy_grid", showindex=False
            )

            click.echo(
                click.style(
                    f"{EMOJIS['sneak']} Sneak Peek: Displaying the first {config.proofreading.cli.show} hits.",
                    fg="bright_magenta",
                )
            )
            click.echo(click.style(table_str, fg="bright_magenta"))

        else:
            click.echo(click.style("No data found for the given filters.", fg="yellow"))

    save(path=file_system, data=hits, filename=RAW_HITS_DATASET_NAME)

    click.echo(
        click.style(
            f"\n{EMOJIS['disc']} Data successfully saved to {file_system}/{RAW_HITS_DATASET_NAME}.",
            fg="green",
            bold=True,
        )
    )


cli.add_command(hits)

if __name__ == "__main__":
    cli()
