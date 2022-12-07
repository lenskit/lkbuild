"""
Support tasks shared across LensKit packages.
"""

from os import fspath, environ
import sys
from pathlib import Path
from invoke import task, Program, Collection
from . import env
import yaml
import requests

__ALL__ = [
    'dev_lock',
    'conda_platform'
]

DATA_DIR = Path('data')
BIBTEX_URL = 'https://paperpile.com/eb/YdOlWmnlit'
BIBTEX_FILE = Path('docs/lenskit.bib')


@task(iterable=['extras', 'mixins'])
def dev_lock(c, platform=None, extras=None, version=None, blas=None, mixins=None, env_file=False,
             filter_extras=True, combined_lock_file=False):
    "Create a development lockfile"
    plat = env.conda_platform()

    build_dir = Path('build')
    build_dir.mkdir(exist_ok=True)

    spec_dir = Path(__file__).parent / 'specs'
    if not spec_dir.exists():
        raise RuntimeError('spec dir not found, is lkbuild installed correctly?')

    cmd = f'conda-lock lock --mamba --dev-dependencies '
    if platform and platform != 'all':
        cmd += f'-p {platform}'
    elif not combined_lock_file:
        cmd += f'-p {plat}'

    if env_file:
        cmd += ' -k env'
    elif not combined_lock_file:
        cmd += ' -k explicit'

    if version:
        fn = f'python-{version}-spec.yml'
        sf = spec_dir / fn
        bf = build_dir / fn
        bf.write_bytes(sf.read_bytes())
        cmd += ' -f ' + fspath(bf)
    if blas:
        fn = f'{blas}-spec.yml'
        sf = spec_dir / fn
        bf = build_dir / fn
        bf.write_bytes(sf.read_bytes())
        cmd += ' -f ' + fspath(bf)

    for m in mixins:
        cmd += f' -f {m}'

    cmd += ' -f pyproject.toml'

    for e in extras:
        cmd += f' -e {e}'

    if filter_extras:
        cmd += ' --filter-extras'

    print('running', cmd, file=sys.stderr)
    c.run(cmd)

    gh_out = environ.get('GITHUB_OUTPUT', None)
    if gh_out:
        print('detected github actions, writing output file')
        with open(gh_out, 'a') as ghof:
            print(f'platform={plat}', file=ghof)
            if env_file:
                fn = f'conda-{plat}.lock.yml'
            else:
                fn = f'conda-{plat}.lock'
            print(f'environment-file={fn}', file=ghof)


@task(iterable=['extras'])
def env_file(c, platform=None, extras=None, version=None, blas=None, dev_deps=True,
             output=None, name=None):
    "Create an unresolved environment file"
    from conda_lock.conda_lock import parse_source_files, aggregate_lock_specs

    if not platform:
        platform = env.conda_platform()

    files = [Path('pyproject.toml')]

    spec_dir = Path(__file__).parent / 'specs'
    if not spec_dir.exists():
        raise RuntimeError('spec dir not found, is lkbuild installed correctly?')

    if version:
        files.append(spec_dir / f'python-{version}-spec.yml')
    if blas:
        files.append(spec_dir / f'{blas}-spec.yml')

    lock = parse_source_files(files, platform, dev_deps, extras)
    lock = aggregate_lock_specs(lock)
    env_spec = {
        'channels': lock.channels,
        'dependencies': lock.specs,
    }
    if name:
        env_spec['name'] = name

    if output:
        print('writing environment to', output, file=sys.stderr)
        out = Path(output)
        with out.open('w') as f:
            yaml.dump(env_spec, f)
    else:
        yaml.dump(env_spec, sys.stdout)


@task
def conda_platform(c, gh_output=False):
    plat = env.conda_platform()
    if gh_output:
        print('::set-output name=conda-platform::' + plat)
    else:
        print(plat)


@task
def update_bibtex(c):
    "Update the BibTeX file"
    res = requests.get(BIBTEX_URL)
    print('updating file', BIBTEX_FILE)
    BIBTEX_FILE.write_text(res.text, encoding='utf-8')


@task
def fetch_data(c, data='ml-100k', data_dir=DATA_DIR):
    "Fetch a data set."
    from . import datasets

    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True, parents=True)
    if data.startswith('ml-'):
        datasets.fetch_ml(DATA_DIR, data)
    else:
        raise ValueError(f'unknown data set {data}')
