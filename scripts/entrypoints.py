import subprocess


def _run(bash_script: str):
    return subprocess.call(bash_script, shell=True)


def dev():
    return _run("./scripts/bash/dev.sh")


def test():
    return _run("./scripts/bash/test.sh")


def test_dev():
    return _run("./scripts/bash/test-dev.sh")


def lint():
    return _run("./scripts/bash/lint.sh")
