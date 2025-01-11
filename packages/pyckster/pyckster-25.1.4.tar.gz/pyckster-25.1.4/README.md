# Pyckster
[![PyPI - Version](https://img.shields.io/pypi/v/pyckster)](https://pypi.org/project/pyckster/)
[![GitLab Tag](https://img.shields.io/gitlab/v/tag/spasquet%2Fpyckster?gitlab_url=https%3A%2F%2Fgitlab.in2p3.fr)](https://gitlab.in2p3.fr/spasquet/pyckster/-/tags)
<!-- ![GitLab Release](https://img.shields.io/gitlab/v/release/spasquet%2Fpyckster?gitlab_url=https%3A%2F%2Fgitlab.in2p3.fr) -->

Pyckster is an open-source PyQt5-based GUI for picking seismic traveltimes. It reads seismic files in SEG2, SEGY and Seismic Unix (SU) formats. Picked traveltimes are saved in [pyGIMLi](https://www.pygimli.org)'s unified format so they can easily be inverted to reconstruct subsurface models of seismic velocity. 

## Installation

You can simply download the package from PyPi:
``` bash
pip install pyckster
```

Or download the sources file in the Gitlab repository and unzip it in the directory of your choice.

## Running Pyckster

If you installed Pyckster with Pypi, open a terminal and run:
```bash
pyckster
```

If you downloaded the source files, open a terminal, move to the `pyckster-master` directory and run:
```bash
python pyckster.py
```

## Author
Pyckster is currently developped by [Sylvain Pasquet](https://orcid.org/0000-0002-3625-9212)\
[sylvain.pasquet@sorbonne-universite.fr](sylvain.pasquet@sorbonne-universite.fr)


*CNRS, Sorbonne Université*\
*UAR 3455 OSU ECCE TERRA*\
*UMR 7619 METIS*


Any feedback or help is welcome.

## Licence

Pyckster is distributed under the terms of the GPLv3 license. Details on
the license agreement can be found [here].

[here]: LICENCE