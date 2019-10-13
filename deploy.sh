#!/usr/bin/env bash
set -e
export VERSION=$(poetry run python -c "import celery_slack; print(celery_slack.__version__)")
poetry build
poetry run twine upload dist/celery_slack-${VERSION}*
git tag -a ${VERSION} -m "${VERSION}"
git push --tags