#!/usr/bin/env bash
set -e

echo "[*] Updating apt..."
sudo apt-get update

echo "[*] Installing system dependencies (Poppler for pdf2image)..."
sudo apt-get install -y \
  poppler-utils  # pdf2image에서 pdftoppm/pdftocairo 사용[web:79][web:82]

echo "[*] Installing Python packages (easyocr, pdf2image, OpenCV)..."
# 필요하면 여기서 venv 활성화하고 진행
pip install --upgrade pip
pip install easyocr pdf2image opencv-python-headless

echo "[*] Done."
echo "[*] 이제 './run.sh \"your.pdf\"' 또는 './run.sh \"dir/*.pdf\"' 로 실행 가능합니다."