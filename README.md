# LensKit build support code

This repository provides support code for use in LensKit builds and development.  If you are trying to
use LensKit, you don't need it; it is only used for working on developing LensKit (and related packages).

To set up a Conda environment that contains the utilities needed to bootstrap a LensKit
development environment:

    conda env create -n lkboot -f https://raw.githubusercontent.com/lenskit/lkbuild/main/boot-env.yml

Then you can run the lkbuild utilities:

    conda activate lkboot
    lkbuild --help

For example, you can create a lock file for developing LensKit:

    lkbuild dev-lock -v 3.9 -b mkl

Or you can download some testing data:

    lkbuild fetch-data -d ml-20m

You can also install into a Python environment with one of:

    pip install lenskit-build-helpers
    conda install -c lenskit lenskit-build-helpers

## GitHub Actions

This repository also provides some GitHub actions to support our CI workflow.

- `actions/setup-env` — sets up an Anaconda environment based on locking the dependencies from `pyproject.toml`.
