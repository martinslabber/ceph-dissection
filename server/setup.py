from setuptools import find_packages, setup

install_requires = ["aiohttp", "aiopg[sa]", "aiohttp-jinja2", "arrow"]

setup(
    name="cephdissectionserver",
    setup_requires=["katversion"],
    use_katversion=True,
    description="Ceph Dissection Server",
    platforms=["POSIX"],
    packages=find_packages(),
    package_data={"": ["templates/*.j2", "static/*.*"]},
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
