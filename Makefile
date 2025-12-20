.PHONY: help install start fmt check fix test clean build-installer

help:
	@echo "利用可能なコマンド:"
	@echo "  make install        - 依存関係のインストール"
	@echo "  make start          - アプリケーションの起動"
	@echo "  make fmt            - コードのフォーマット"
	@echo "  make check          - 静的解析・Lint"
	@echo "  make fix            - Lintエラーの自動修正"
	@echo "  make test           - テストの実行"
	@echo "  make clean          - ビルドファイルのクリーンアップ"
	@echo "  make build-installer - インストーラーの作成"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

start:
	python -m n_line

fmt:
	ruff format .

check:
	ruff check .

fix:
	ruff check . --fix

test:
	pytest

clean:
	python scripts/build_installer.py --clean

build-installer:
	python scripts/build_installer.py
