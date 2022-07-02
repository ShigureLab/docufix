VERSION := `poetry run python -c "import sys; from docufix import __version__ as version; sys.stdout.write(version)"`

test:
  poetry run pytest --workers auto
  just clean

fmt:
  poetry run isort .
  poetry run black .

fmt-docs:
  poetry run docufix '**/*.md'
  poetry run docufix '**/*.rst'

build:
  poetry build

publish:
  touch docufix/py.typed
  poetry publish --build
  git tag "v{{VERSION}}"
  git push --tags
  just clean-builds

clean:
  find . -name "*.pyc" -print0 | xargs -0 rm -f
  rm -rf .pytest_cache/
  rm -rf .mypy_cache/
  find . -maxdepth 3 -type d -empty -print0 | xargs -0 -r rm -r

clean-builds:
  rm -rf build/
  rm -rf dist/
  rm -rf *.egg-info/

docs-build:
  poetry run sphinx-apidoc -f -o docs/api/en docufix
  poetry run sphinx-build -D language='cn' docs/ docs/dist

docs-preview:
  pnpm dlx serve docs/dist

docs-clean:
  rm -rf docs/dist/

docs-init-locales:
  poetry run sphinx-build -b gettext docs/ docs/dist/locale

docs-update-locales:
  poetry run sphinx-intl update -p docs/dist/locale -d docs/locales -l cn
