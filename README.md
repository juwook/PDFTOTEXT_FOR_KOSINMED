# PDF OCR CLI (EasyOCR 기반)

PDFTOTEXT writes .txt files extracting all text from .pdf file.
You can extract text, transfer to Your own AI module, and then make problem bank yourself.

---

## Features

- PDF → 이미지 변환 후 EasyOCR로 텍스트 추출
- 한 번에 여러 PDF 처리 (`"dir/*.pdf"` 패턴 지원)
- 원본 파일명을 유지한 `.txt` 결과 생성
- Ubuntu 환경 기준 셋업 스크립트 제공

---

## Project Structure

- `ocr_pdf_easyocr.py` – 메인 CLI 스크립트
- `dependency_install.sh` – 시스템/파이썬 의존성 설치 스크립트
- `run.sh` – 간단 실행 래퍼 (패턴/환경변수 지원)
- `workspace/` – 실제 PDF와 출력 텍스트를 두는 작업 디렉토리 (Git ignore)

---

## Installation

```bash
chmod +x dependency_install.sh run.sh
./dependency_install.sh
```

Python 가상환경을 사용할 경우, 활성화 후 위 스크립트를 실행하세요.

---

## Usage

### 단일 PDF

```bash
./run.sh "workspace/<your file>.pdf"
```

### 폴더 전체 PDF

```bash
./run.sh "workspace/*.pdf"
```

### 출력 디렉토리/언어 설정

```bash
OUT_DIR=out_txt LANGS="ko en" ./run.sh "slides/*.pdf"
```

생성된 결과는 원본 파일명에 `.txt` 확장자를 붙여서 저장됩니다.

---

## Notes

- OCR 품질은 원본 PDF 스캔 품질과 dpi 설정에 따라 달라집니다.
- 기본 설정은 영어+한글 혼합 강의 슬라이드를 대상으로 조정되었습니다.
- 더 높은 품질이 필요하면 `--dpi 600` 이상으로 조정하거나 전처리 단계 추가를 고려하세요. (현재 600으로 맞춰놓은 상태)