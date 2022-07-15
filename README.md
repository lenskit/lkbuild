# LensKit build support code

This repository provides support code for use in LensKit builds and development.

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

You can also install into a Python environment with:

    lenskit-build-helpers