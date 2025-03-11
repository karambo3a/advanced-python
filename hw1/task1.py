import click


@click.command()
@click.argument("files", nargs=-1, type=click.File("r"))
def nl(files: click.File):
    if not files:
        files = [click.get_text_stream("stdin")]

    line_number = 1
    for file in files:
        for line in file:
            click.echo(f"{line_number:6d}  {line}", nl=False)
            line_number += 1

if __name__ == "__main__":
    nl()
