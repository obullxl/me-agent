import fitz
import os


def pdf_to_images(pdf_path, output_folder, zoom=2.0):
    """将单个PDF文件转换为图片"""
    pdf_document = fitz.open(pdf_path)

    # 提取 PDF 文件名（不带 .pdf 后缀）作为图片前缀和子文件夹名
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # 为该PDF创建专属的子文件夹，防止图片混杂在一起
    pdf_output_dir = os.path.join(output_folder, pdf_name)
    if not os.path.exists(pdf_output_dir):
        os.makedirs(pdf_output_dir)

    print(f"\n开始转换: {pdf_name}.pdf (共 {len(pdf_document)} 页)")

    for page_num in range(len(pdf_document)):
        # 获取第page_num页
        page = pdf_document.load_page(page_num)

        # 使用 Matrix 矩阵进行缩放
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # 定义输出路径：保存在对应的子文件夹中
        output_path = os.path.join(
            pdf_output_dir, f"{pdf_name}_page_{page_num + 1}.png"
        )

        # 保存图片
        pix.save(output_path)

    pdf_document.close()
    print(f"✅ {pdf_name}.pdf 转换完成！")


def batch_convert_pdfs(pdf_dir, output_folder, zoom=2.0):
    """批量转换指定目录下的所有PDF文件"""
    # 确保图片根目录存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 筛选出目录下所有的PDF文件
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"⚠️ 警告：在目录 {pdf_dir} 下没有找到任何PDF文件！")
        return

    print(f"📂 在目录 {pdf_dir} 中共找到 {len(pdf_files)} 个PDF文件，开始批量转换...")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        # 调用单文件转换函数
        pdf_to_images(pdf_path, output_folder, zoom)


# 使用示例
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(script_path)

    # 指定你的 PDF 存放目录
    pdf_input_dir = os.path.join(current_dir, "files")

    # 指定图片输出的根目录（与PDF目录相同层级）
    image_output_dir = os.path.join(pdf_input_dir, "images")

    # 执行批量转换，设置 zoom=3.0 保证高清
    batch_convert_pdfs(pdf_input_dir, image_output_dir, zoom=3.0)
