#!/usr/bin/env python
import argparse
import glob
from pathlib import Path

import numpy as np
from pdf2image import convert_from_path
import easyocr


def ocr_pdf_with_easyocr(
    pdf_path: Path,
    reader: easyocr.Reader,
    dpi: int = 300,
) -> str:
    """
    PDF를 페이지별 이미지로 변환한 뒤,
    EasyOCR로 각 페이지의 텍스트를 추출해서 하나의 문자열로 반환.
    """
    pages = convert_from_path(str(pdf_path), dpi=dpi)
    texts = []

    for i, page in enumerate(pages, start=1):
        # PIL.Image -> numpy array
        np_img = np.array(page)

        # EasyOCR로 텍스트만 가져오기 (detail=0이면 텍스트 리스트만 반환)[web:108][web:125]
        results = reader.readtext(np_img, detail=0)

        page_text = "\n".join(results)
        texts.append(f"\n\n===== Page {i} ({pdf_path.name}) =====\n\n{page_text}")

    return "".join(texts)


def process_one_pdf(
    pdf_path: Path,
    reader: easyocr.Reader,
    dpi: int,
    out_dir: Path | None,
):
    if not pdf_path.is_file():
        print(f"[SKIP] 파일 아님: {pdf_path}")
        return

    # 출력 파일명: 원래 파일명 그대로, 확장자만 .txt로 변경
    if out_dir is None:
        out_path = pdf_path.with_suffix(".txt")
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / pdf_path.with_suffix(".txt").name

    print(f"[OCR] {pdf_path} → {out_path}")
    text = ocr_pdf_with_easyocr(pdf_path, reader=reader, dpi=dpi)
    out_path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="EasyOCR + pdf2image 기반 PDF → txt OCR 도구"
    )
    parser.add_argument(
        "input",
        help="입력 파일/패턴 (예: doc.pdf, 'test/*.pdf')",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="PDF → 이미지 변환 DPI (기본: 300, 품질 문제시 400 추천)",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help="결과 txt를 저장할 디렉토리 (기본: 각 PDF와 같은 위치)",
    )
    parser.add_argument(
        "--langs",
        nargs="+",
        default=["ko", "en"],
        help="EasyOCR 언어 리스트 (예: ko en, en, ja en 등; 기본: ko en)",  # [web:108][web:127]
    )

    args = parser.parse_args()

    # EasyOCR Reader 한 번만 생성해서 재사용
    print(f"[*] Initializing EasyOCR with languages: {args.langs}")
    reader = easyocr.Reader(args.langs, gpu=False)  # GPU 쓰면 gpu=True로 변경[web:108][web:116]

    # glob 패턴 지원: test/*.pdf 등[web:54][web:59]
    paths = [Path(p) for p in glob.glob(args.input)]
    if not paths:
        p = Path(args.input)
        if p.is_file():
            paths = [p]
        else:
            raise FileNotFoundError(f"입력에 매칭되는 PDF가 없습니다: {args.input}")

    out_dir = Path(args.out_dir) if args.out_dir else None

    for pdf_path in paths:
        if pdf_path.suffix.lower() != ".pdf":
            print(f"[SKIP] PDF 아님: {pdf_path}")
            continue
        process_one_pdf(
            pdf_path=pdf_path,
            reader=reader,
            dpi=args.dpi,
            out_dir=out_dir,
        )


if __name__ == "__main__":
    main()