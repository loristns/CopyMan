import click  # Command line interface framework
import shutil  # File system utilities
import os.path
import errno  # Exception identification
import tarfile  # Archive and compression formats
import zipfile

# FTP server library
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


@click.group()
def cli():
    """
    Welcome to CopyMan V2 !

    The CLI tool for copy, compress and shares files and folders easily !
    """
    pass


@cli.command('gather')
@click.option('--destination', '-d', type=click.Path(exists=True, dir_okay=True), prompt="Destination folder path",
              help="The folder where all file will be copied.")
@click.option('--sources', '-s', type=click.Path(exists=True), multiple=True,
              help="All the files/folders to copy.")
@click.option('--ignore', '-i', default="", multiple=True, help="Filenames and patterns to ignore in folders copy.")
def gather(destination, sources, ignore):
    """Gather files in a same destination."""

    destination = click.format_filename(destination)  # Convert Path to string

    with click.progressbar(sources) as copy_bar:
        for data in copy_bar:
            data = click.format_filename(data)  # Here too

            try:
                shutil.copytree(data, "{}/{}".format(destination, data), ignore=shutil.ignore_patterns(*ignore))
                click.echo(" Folder '{}' successfully copied in destination folder.".format(data))

            except OSError as dir_error:
                if dir_error.errno == errno.ENOTDIR:  # If data is a file, not a directory
                    shutil.copy(data, destination)
                    click.echo(" File '{}' successfully copied in destination folder.".format(data))
                else:
                    click.echo(" Error : Python {}".format(dir_error))


@cli.command('targz')
@click.option('--name', '-n', type=click.Path(), default="Package.tar.gz",
              help="The file where all file will be packaged and compressed.")
@click.option('--sources', '-s', type=click.Path(exists=True), multiple=True,
              help="All the files/folders to package.")
def archive_targz(name, sources):
    """Gather files in a .tar.gz package."""

    name = click.format_filename(name)

    with tarfile.open(name, "w:gz") as tar_file:
        with click.progressbar(sources) as tar_bar:
            for data in tar_bar:
                data = click.format_filename(data)

                tar_file.add(data, arcname=os.path.basename(data))
                click.echo(" '{}' successfully packaged and compressed.".format(os.path.basename(data)))


@cli.command('zip')
@click.option('--name', '-n', type=click.Path(), default="Package.zip",
              help="The file where all file will be zipped.")
@click.option('--sources', '-s', type=click.Path(exists=True), multiple=True,
              help="All the files/folders to zip.")
def archive_zip(name, sources):
    """Gather files in a zip package."""

    name = click.format_filename(name)

    with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        with click.progressbar(sources) as zip_bar:
            for data in zip_bar:
                data = click.format_filename(data)

                zip_file.write(data, arcname=os.path.basename(data))
                click.echo(" '{}' successfully zipped.".format(os.path.basename(data)))


@cli.command('serve')
@click.option('--ip', default="127.0.0.1", help="IP address to serve.")
@click.option('--port', default=2221, help="Port to serve.")
@click.option('--directory', type=click.Path(exists=True, dir_okay=True), help="Directory to serve.")
def serve(ip, port, directory):
    """Serve files on a FTP server."""

    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(click.format_filename(directory))
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer((ip, port), handler)

    click.echo("FTP Server successfully configurated at {}:{}.".format(ip, port))
    server.serve_forever()

if __name__ == '__main__':
    cli()
