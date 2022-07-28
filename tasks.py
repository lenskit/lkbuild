"""
Tasks for maintaining the LensKit build tools.  These tasks are for the build
tools only, not for LensKit projects built with these tools --- the
`lkbuild.tasks` package has those actions.
"""

from invoke import task


@task
def update_lockfile(c, use_mamba=True):
    "Re-lock the project dependencies"
    mamba_opt = '--mamba' if use_mamba else ''
    c.run(f'conda-lock lock {mamba_opt} -f pyproject.toml')


@task
def render_lockfiles(c):
    tmpl = 'actions/setup-conda-env/conda-{platform}.lock'
    c.run(f'conda-lock render --filename-template={tmpl}')
