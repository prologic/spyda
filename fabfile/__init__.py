# Package:  fabfile
# Date:     18th June 2013
# Author:   James Mills, j dot mills at griffith dot edu dot au


"""Development Tasks"""


from __future__ import print_function

from os import getcwd


from fabric.api import abort, cd, execute, hide, hosts
from fabric.api import local, prefix, prompt, run, settings, task


import help  # noqa
import docs  # noqa
from .utils import msg, pip, requires, tobool


@task()
@requires("pip")
def build(**options):
    """Build and install required dependencies

    Options can be provided to customize the build.
    The following options are supported:

    - dev -> Whether to install in development mode (Default: Fase)
    """

    dev = tobool(options.get("dev", False))

    pip(requirements="requirements{0:s}.txt".format("-dev" if dev else ""))

    with settings(hide("stdout", "stderr"), warn_only=True):
        local("python setup.py {0:s}".format("develop" if dev else "install"))


@task()
def clean():
    """Clean up build files and directories"""

    files = ["build", ".converage", "coverage", "dist", "docs/build", "*.xml"]

    local("rm -rf {0:s}".format(" ".join(files)))

    local("find . -type f -name '*~' -delete")
    local("find . -type f -name '*.pyo' -delete")
    local("find . -type f -name '*.pyc' -delete")
    local("find . -type d -name '__pycache__' -delete")
    local("find . -type d -name '*egg-info' -exec rm -rf {} +")


@task()
def develop():
    """Build and Install in Development Mode"""

    return execute(build, dev=True)


@task()
@requires("py.test")
def test():
    """Run all unit tests and doctests."""

    local("python setup.py test")


@task()
@requires("docker")
def docker(**options):
    """Build and Publish Docker Image

    Options can be provided to customize the build.
    The following options are supported:

    - rebuild -> Whether to rebuild without a cache.
    """

    rebuild = tobool(options.get("rebuild", False))

    with msg("Building Image"):
        if rebuild:
            local("docker build -t prologic/spyda --no-cache .")
        else:
            local("docker build -t prologic/spyda .")

    with msg("Pushing Image"):
        local("docker push  prologic/spyda")


@task()
@hosts("localhost")
def release():
    """Performs a full release"""

    with cd(getcwd()):
        with msg("Creating env"):
            run("mkvirtualenv test")

        with msg("Bootstrapping"):
            with prefix("workon test"):
                run("./bootstrap.sh")

        with msg("Building"):
            with prefix("workon test"):
                run("fab develop")

        with msg("Running tests"):
            with prefix("workon test"):
                run("fab test")

        with msg("Building docs"):
            with prefix("workon test"):
                run("pip install -r docs/requirements.txt")
                run("fab docs")

        version = run("python setup.py --version")
        if "dev" in version:
            abort("Detected Development Version!")

        print("Release version: {0:s}".format(version))

        if prompt("Is this ok?", default="n", validate=r"^[YyNn]?$") in "yY":
            with prefix("workon test"):
                run("hg tag {0:s}".format(version))
                run("python setup.py egg_info sdist bdist_egg register upload")
                run("python setup.py build_sphinx upload_sphinx")

        with msg("Destroying env"):
            run("rmvirtualenv test")


@task()
def sync(*args):
    """Synchronouse Local Repository with Remote(s)"""

    status = local("hg status", capture=True)
    if status:
        abort(
            (
                "Repository is not in a clean state! "
                "Please commit, revert or shelve!"
            )
        )

    with settings(warn_only=True):
        local("hg fetch")
        local("hg fetch github")
        local("hg push")
        local("hg bookmark -r tip master")
        local("hg push github")
