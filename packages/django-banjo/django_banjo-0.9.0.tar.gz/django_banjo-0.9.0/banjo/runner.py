import os
from os.path import abspath, dirname, join
import sys
import django
import shutil
from pathlib import Path
from subprocess import run
from django.conf import settings
from django.core import management

sys.path.insert(0, '.')

def setup_django(debug=False, settings=None, clean=False):
    """Sets up Django and runs prerequisite management commands.

    Django needs to be configured before any app-specific code can be loaded.
    Sets the environment variable ``DJANGO_SETTINGS_MODULE`` so Django uses one of 
    Banjo's settings modules (and so the user's app doesn't need a settings file). 
    Then runs ``django.setup()``. 

    Imports the app's views module, which 
    causes banjo's route_get and route_post decorators to be invoked, 
    which populates ``banjo.urls:urlpatterns``.

    Finally, executes Django management commands ``makemigrations`` and ``migrate``, 
    ensuring that the database is in sync with the app's models.
    """
    if settings:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    elif debug:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings_debug')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings')
    django.setup()

    if clean:
        from django.conf import settings
        Path(settings.DATABASES["default"]["NAME"]).unlink()
        if Path("app/migrations").exists():
            shutil.rmtree("app/migrations")

    from app import views

    management.execute_from_command_line(['', 'makemigrations', 'app', 'banjo'])
    management.execute_from_command_line(['', 'migrate'])

def main():
    """The entry point for the Banjo CLI. 
    Declares arguments and then invokes Django management commands. Passing ``--clean``
    will delete the database and all migrations, which is the simplest way to resolve
    some complex migration states or other issues when the database content doesn't matter.
    If ``--shell``, invokes ``shell_plus``, otherwise invokes ``runserver``, passing along 
    ``--port`` and ``--debug`` options.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-s", "--shell", action="store_true")
    parser.add_argument("-p", "--port", type=int, default=8000)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-c", "--clean", action="store_true")
    parser.add_argument("-m", "--settings")
    args = parser.parse_args()
    setup_django(args.debug, settings=args.settings, clean=args.clean)
    if args.shell:
        management.execute_from_command_line(['', 'shell_plus'])
    else:
        management.execute_from_command_line(['', 'runserver', str(args.port)])
