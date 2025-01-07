.PHONY: help clean build install test dev-setup version bump-patch bump-minor bump-major publish test-publish release-patch release-minor release-major init-git

help:
	@echo "Available commands:"
	@echo "  make init-git       - Initialize git repository"
	@echo "  make dev-setup      - Install development dependencies"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make build          - Build the package"
	@echo "  make install        - Install package locally"
	@echo "  make version        - Show current version"
	@echo "  make bump-patch     - Bump patch version (0.0.X)"
	@echo "  make bump-minor     - Bump minor version (0.X.0)"
	@echo "  make bump-major     - Bump major version (X.0.0)"
	@echo "  make test-publish   - Publish to Test PyPI"
	@echo "  make publish        - Publish to PyPI"
	@echo "  make release-patch  - Bump patch version and publish"
	@echo "  make release-minor  - Bump minor version and publish"
	@echo "  make release-major  - Bump major version and publish"

init-git:
	@if [ ! -d .git ]; then \
		git init; \
		git add .; \
		git config --local user.email "you@example.com"; \
		git config --local user.name "Your Name"; \
		git commit -m "Initial commit"; \
	fi

dev-setup: init-git
	python3 -m pip install --upgrade pip
	python3 -m pip install -e ".[dev]"
	python3 -m pip install build twine pytest bump2version

clean:
	rm -rf dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python3 -m build

install: clean
	python3 -m pip install -e .

test:
	python3 -m pytest

version:
	@python3 -c "from pygsm import __version__; print(__version__)"

bump-patch: init-git
	bump2version patch --allow-dirty
	git push || true
	git push --tags || true

bump-minor: init-git
	bump2version minor --allow-dirty
	git push || true
	git push --tags || true

bump-major: init-git
	bump2version major --allow-dirty
	git push || true
	git push --tags || true

test-publish: build
	python3 -m twine upload --repository testpypi dist/*

publish: build
	python3 -m twine upload dist/*

release-patch: bump-patch publish

release-minor: bump-minor publish

release-major: bump-major publish 