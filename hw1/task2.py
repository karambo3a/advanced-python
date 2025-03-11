import click


@click.command()
@click.argument("files", nargs=-1, type=click.File("r"))
def tail(files: tuple[click.File, ...]):
    lines_cnt = 10

    if not files:
        files = [click.get_text_stream("stdin")]
        lines_cnt = 17

    for i, file in enumerate(files):
        if len(files) > 1:
            click.echo(f"==> {file.name} <==")
        click.echo("".join(file.readlines()[-lines_cnt:]), nl=False)
        if i != len(files) - 1:
            click.echo()


if __name__ == "__main__":
    tail()
