from setuptools import setup, find_packages

setup(
    name="infmysql",
    version="0.0.1",
    author="Bifer Team",
    description="Simple MySQL client",
    platforms="Linux",
    packages=find_packages(exclude=["specs", "integration_specs"]),
    install_requires=[
        "mysqlclient==2.1.0",
        "retrying==1.3.3",
        "infcommon",
    ],
    dependency_links=[
        "git+https://github.com/aleasoluciones/infcommon3.git#egg=infcommon"
    ],
)
