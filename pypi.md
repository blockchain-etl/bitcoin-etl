# Uploading to PYPI

Create `$HOME/.pypirc` with the following content:

```
[distutils]
index-servers=
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = <username>
password = <password>

[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```

Run the following to install to test pypi:

```bash
> python setup.py sdist
> twine upload dist/* -r testpypi
> pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple bitcoin-etl 
```

Run the following to install to pypi:

```bash
> python setup.py sdist
> twine upload dist/* 
> pip install bitcoin-etl 
```
