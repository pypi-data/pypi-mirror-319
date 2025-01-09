from setuptools import setup, find_packages

setup(
    name="pyckster",
    description="A PyQt5-based GUI for picking seismic traveltimes",
    author="Sylvain Pasquet",
    author_email="sylvain.pasquet@sorbonne-universite.fr",
    version="25.01",
    url='https://gitlab.in2p3.fr/spasquet/pyckster',
    license='GPLv3',
    # packages=['pyckster'],
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.4",
        "pyqtgraph",
        "numpy",
        "matplotlib",
        "obspy",
    ],
    include_package_data=True,
      zip_safe=False
)