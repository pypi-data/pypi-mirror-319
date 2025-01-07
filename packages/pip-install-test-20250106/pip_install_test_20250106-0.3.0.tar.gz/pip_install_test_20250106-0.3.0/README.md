1. poetry config repositories.pypi https://upload.pypi.org/legacy/
2. $env:PYPI_USERNAME="__token__"
3. $env:PYPI_PASSWORD="<api-token>"
4. poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
