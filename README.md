# audio2summary

## 概要

音声ファイルから文字起こしを行い、要約したテキストを生成するスクリプトです。

## 実行方法

- `download-model.py`: 話者分離に利用するpyannoteのモデルをダウンロードします。
- `speech-to-text.py`: 指定した音源ファイルから文字起こしを行います。
- `speech-to-text-finder.py`: 指定したフォルダ内から音源ファイルを探索し、文字起こしを行います。

## ローカル環境の構築

事前に下記が利用できるように環境を設定してください。

- [node.js](https://nodejs.org/en): 開発環境のlinterに利用します。
- [python](https://nodejs.org/en)
- [task](https://taskfile.dev/): タスクランナーとして利用します。

仮想環境などの構築は下記のコマンドで実行します。

```sh
# スクリプト実行などのための仮想環境などを作成
task init
# whisper.cpp, llama.cppのビルド
task build
```

## Taskfile

実行可能なタスク一覧は下記のコマンドで確認してください。

```sh
task -l
```

## code style

コードの整形などはは下記を利用しています。

- json, markdown, toml, yaml
  - [prettier](https://prettier.io/): formatter
- python
  - [ruff](https://github.com/astral-sh/ruff): python linter and formatter.
  - [mypy](https://github.com/python/mypy): static typing.
  - docstring: [numpy 形式](https://numpydoc.readthedocs.io/en/latest/format.html)を想定しています。
    - vscodeの場合は[autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)拡張機能によりひな型を自動生成できます。

## Tips
