# appteka - helpers collection

# Copyright (C) 2018-2025 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup
from appteka import __version__


def _read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname),
              encoding='utf-8') as buf:
        return buf.read()


setup(
    name="appteka",
    version=__version__,
    description="All goods",
    author="Aleksandr Popov",
    author_email="aleneus@gmail.com",
    license="LGPLv3",
    keywords="application, gui",
    url="https://github.com/aleneus/appteka",
    long_description=_read('README'),
    packages=['appteka', 'appteka.pyqt', 'appteka.sqlite'],
    install_requires=[
        'PyQt5>=5.15.2',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
