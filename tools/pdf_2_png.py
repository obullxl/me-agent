import argparse
import fitz
import os


def pdf_to_images(pdf_path, zoom=2.0):
    """将单个PDF文件转换为图片，输出到PDF所在目录。"""
    pdf_document = fitz.open(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_dir = os.path.dirname(pdf_path)

    print(f"\n开始转换: {pdf_name}.pdf (共 {len(pdf_document)} 页)")

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        output_path = os.path.join(
            pdf_dir, f"{pdf_name}-{page_num + 1:03d}.png"
        )
        pix.save(output_path)

    pdf_document.close()
    print(f"✅ {pdf_name}.pdf 转换完成！ 输出目录: {pdf_dir}")


def batch_convert_pdfs(pdf_dir, zoom=2.0):
    """批量转换指定目录下的所有PDF文件。"""
    if not os.path.isdir(pdf_dir):
        print(f"❌ 错误：{pdf_dir} 不是一个有效目录。")
        return

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"⚠️ 警告：在目录 {pdf_dir} 下没有找到任何PDF文件！")
        return

    print(f"📂 在目录 {pdf_dir} 中共找到 {len(pdf_files)} 个PDF文件，开始批量转换...")
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        pdf_to_images(pdf_path, zoom)


def main():
    parser = argparse.ArgumentParser(
        description="将指定目录中的 PDF 文件转换为 PNG 图像，输出到原 PDF 所在目录。"
    )
    parser.add_argument(
        "path",
        help="待处理的 PDF 文件目录，或单个 PDF 文件路径。",
    )
    parser.add_argument(
        "--zoom",
        type=float,
        default=2.0,
        help="图像缩放倍数，默认 2.0，可选更高清，例如 3.0。",
    )

    args = parser.parse_args()
    target_path = os.path.abspath(args.path)

    if os.path.isdir(target_path):
        batch_convert_pdfs(target_path, zoom=args.zoom)
    elif os.path.isfile(target_path) and target_path.lower().endswith(".pdf"):
        pdf_to_images(target_path, zoom=args.zoom)
    else:
        print(f"❌ 错误：{args.path} 不是有效的 PDF 目录或 PDF 文件。")


if __name__ == "__main__":
    main()
