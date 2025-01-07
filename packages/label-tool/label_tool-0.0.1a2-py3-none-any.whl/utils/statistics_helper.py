from typing import List
import click


def statistics_helper(successful_count: int, failed_files: List[str]) -> None:
  click.secho(f"successful count:{successful_count}", fg="green")
  click.secho(f"fail count: {len(failed_files)}", fg="red")
  click.secho(f"fail file {failed_files}")
