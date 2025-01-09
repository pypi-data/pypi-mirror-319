from setuptools import setup

setup(
    name="co2114",
    version="0.1",
    description="codebase for co2114",
    author="wil ward",
    packages=[
        "co2114",
        "co2114.agent", 
        "co2114.search", 
        "co2114.optimisation",
        "co2114.constraints", 
        "co2114.constraints.csp",
        "co2114.util"],
    install_requires=['pygame', 'numpy', 'ipython', 'matplotlib', 'jupyter']
)
