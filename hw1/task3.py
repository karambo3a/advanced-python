import click
import sys


@click.command()
@click.argument("files", nargs=-1, type=click.File("r"))
def wc(files: tuple[click.File, ...]):
    total_lines, total_words, total_bytes = 0, 0, 0
    if not files:
        files = [click.get_text_stream("stdin")]

    for file in files:
        lines_cnt, words_cnt, bytes_cnt = 0, 0, 0
        for line in file:
            lines_cnt += 1
            words_cnt += len(line.split())
            bytes_cnt += len(line.encode("utf-8"))
        file_name = file.name if file != sys.stdin else ""
        click.echo(f"{lines_cnt:10d} {words_cnt:10d} {bytes_cnt:10d} {file_name}")
        if len(files) > 1:
            total_lines += lines_cnt
            total_words += words_cnt
            total_bytes += bytes_cnt

    if len(files) > 1:
        click.echo(f"{total_lines:10d} {total_words:10d} {total_bytes:10d} total")


if __name__ == "__main__":
    wc()
