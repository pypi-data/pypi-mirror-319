import os
import platform
from distutils.sysconfig import get_config_var
from typing import Any
from typing import Dict

import numpy
from Cython.Build import cythonize
from setuptools import Extension
from setuptools import find_packages
from setuptools import setup
from setuptools_rust import RustExtension

LIBRARY = "opteryx"


def is_mac():  # pragma: no cover
    return platform.system().lower() == "darwin"


COMPILE_FLAGS = ["-O2"] if is_mac() else ["-O2", "-march=native"]

# Dynamically get the default include paths
include_dirs = [numpy.get_include()]

# Get the C++ include directory
includedir = get_config_var('INCLUDEDIR')
if includedir:
    include_dirs.append(os.path.join(includedir, 'c++', 'v1'))  # C++ headers path

# Get the Python include directory
includepy = get_config_var('INCLUDEPY')
if includepy:
    include_dirs.append(includepy)

# Check if paths exist
include_dirs = [p for p in include_dirs if os.path.exists(p)]

def rust_build(setup_kwargs: Dict[str, Any]) -> None:
    setup_kwargs.update(
        {
            "rust_extensions": [RustExtension("opteryx.compute", "Cargo.toml", debug=False)],
            "zip_safe": False,
        }
    )


__author__ = "notset"
__version__ = "notset"
with open(f"{LIBRARY}/__version__.py", mode="r") as v:
    vers = v.read()
exec(vers)  # nosec

with open("README.md", mode="r", encoding="UTF8") as rm:
    long_description = rm.read()

try:
    with open("requirements.txt", "r") as f:
        required = f.read().splitlines()
except:
    with open(f"{LIBRARY}.egg-info/requires.txt", "r") as f:
        required = f.read().splitlines()

extensions = [
    Extension(
        name="opteryx.third_party.fuzzy.csoundex",
        sources=["opteryx/third_party/fuzzy/csoundex.pyx"],
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.levenshtein.clevenshtein",
        sources=["opteryx/compiled/levenshtein/clevenshtein.pyx"],
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.list_ops.cython_list_ops",
        sources=[
            "opteryx/compiled/list_ops/cython_list_ops.pyx",
        ],
        include_dirs=include_dirs,
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.cross_join.cython_cross_join",
        sources=["opteryx/compiled/cross_join/cython_cross_join.pyx"],
        include_dirs=include_dirs,
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.functions.ip_address",
        sources=["opteryx/compiled/functions/ip_address.pyx"],
        include_dirs=include_dirs,
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.structures.hash_table",
        sources=["opteryx/compiled/structures/hash_table.pyx"],
        include_dirs=include_dirs,
        language="c++",
        extra_compile_args=COMPILE_FLAGS + ["-std=c++17"],
    ),
    Extension(
        name="opteryx.compiled.functions.vectors",
        sources=["opteryx/compiled/functions/vectors.pyx"],
        include_dirs=include_dirs,
        language="c++",
        extra_compile_args=COMPILE_FLAGS + ["-std=c++17"],
    ),
    Extension(
        name="opteryx.compiled.functions.functions",
        sources=["opteryx/compiled/functions/functions.pyx"],
        include_dirs=include_dirs,
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.structures.node",
        sources=["opteryx/compiled/structures/node.pyx"],
        extra_compile_args=COMPILE_FLAGS,
    ),
    Extension(
        name="opteryx.compiled.structures.memory_pool",
        sources=["opteryx/compiled/structures/memory_pool.pyx"],
        language="c++",
        extra_compile_args=COMPILE_FLAGS,
    ),
]

setup_config = {
    "name": LIBRARY,
    "version": __version__,
    "description": "Python SQL Query Engine",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "maintainer": "@joocer",
    "author": __author__,
    "author_email": "justin.joyce@joocer.com",
    "packages": find_packages(include=[LIBRARY, f"{LIBRARY}.*"]),
    "python_requires": ">=3.9",
    "url": "https://github.com/mabel-dev/opteryx/",
    "install_requires": required,
    "ext_modules": cythonize(extensions),
    "entry_points": {
        "console_scripts": ["opteryx=opteryx.command:main"],
    },
    "package_data": {
        "": ["*.pyx", "*.pxd"],
    },
}

rust_build(setup_config)

setup(**setup_config)
