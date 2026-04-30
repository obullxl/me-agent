import fitz
import os


def pdf_to_images(pdf_path, output_folder, zoom=2.0):
    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)

    # 核心优化：提取 PDF 文件名（不带 .pdf 后缀）作为图片前缀
    # os.path.basename(pdf_path) 会提取出 "invoice.pdf"
    # os.path.splitext(...)[0] 会去掉后缀，得到 "invoice"
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(len(pdf_document)):
        # 获取第page_num页
        page = pdf_document.load_page(page_num)

        # 使用 Matrix 矩阵进行缩放
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # 定义输出路径：使用提取出的 pdf_name 作为前缀
        output_path = f"{output_folder}/{pdf_name}_page_{page_num + 1}.png"

        # 保存图片
        pix.save(output_path)
        print(f"Page {page_num + 1} saved as {output_path}")


# 使用示例
script_path = os.path.abspath(__file__)
path = os.path.dirname(script_path)
print(f"当前目录: {path}")

# 确保输出文件夹存在
output_folder = f"{path}/files/images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

pdf_path = f"{path}/files/invoice.pdf"
pdf_to_images(pdf_path, output_folder, zoom=3.0)
