import setuptools



description = r"""Python library to extract the current windows environment (ignores the session)."""

setuptools.setup(
    name="winenv",
    packages = setuptools.find_packages(exclude=["tests*"]),
    version="1.0.1",
    description=description,
    author = "Henry Weickert",
    author_email = "henryweickert@gmail.com",
    url = "https://github.com/hweickert/winenv",
    keywords = [],
    entry_points={},
    install_requires=[]
)
