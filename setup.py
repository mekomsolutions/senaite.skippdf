from setuptools import find_packages
from setuptools import setup


setup(
    name="senaite.skippdf",
    version="1.0.0a1",
    description="An add-on to customize SENAITE publish action",
    license="MPL-2.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["senaite"],
    include_package_data=True,
    package_data={"senaite.skippdf": ["*.zcml"]},
    zip_safe=False,
    install_requires=["setuptools", "senaite.core", "zope.interface"],
    entry_points={"z3c.autoinclude.plugin": ["target = plone"]},
)
