from setuptools import setup, find_packages

setup(name="infmysql",
      version="0.0.1",
      author="Bifer Team",
      description="Simple mysql client",
      platforms="Linux",
      packages=find_packages(
          exclude=["tests", "specs", "integration_specs", "functional_specs", "acceptance_specs"]),
      install_requires=[
          'mysqlclient==1.4.1',
          'retrying==1.3.3',
      ],
      extras_require={
          'dev': [
              'packaging@https://github.com/aleasoluciones/pydevlib.git#egg=pydevlib',
          ],
      },
      dependency_links=[])
