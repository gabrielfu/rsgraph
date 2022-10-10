from setuptools import setup, find_packages
from setuptools_rust import Binding, RustExtension

setup(
    name="rsgraph",
    version="0.1",
    rust_extensions=[RustExtension("rsgraph.rsgraphlib", path="Cargo.toml", binding=Binding.PyO3)],
    packages=["rsgraph"],
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "numpy==1.23.3",
    ],
)
