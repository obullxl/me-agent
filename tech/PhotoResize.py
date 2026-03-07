from PIL import Image
import math

def resize_to_1inch_photo(input_path, output_path, dpi=300):
    """
    将图片按比例缩放到1寸标准尺寸（2.54cm × 3.81cm）
    
    参数：
    input_path: 输入图片路径（如"photo.jpg"）
    output_path: 输出图片路径（如"1inch_photo.jpg"）
    dpi: 打印分辨率（默认300DPI，证件照常用）
    """
    # 1寸照片标准尺寸（厘米）
    inch1_width_cm = 2.54
    inch1_height_cm = 3.81
    
    # 厘米转像素（1英寸=2.54厘米，像素数=厘米数/2.54 * DPI）
    target_width = int(inch1_width_cm / 2.54 * dpi)
    target_height = int(inch1_height_cm / 2.54 * dpi)
    
    try:
        # 打开图片
        img = Image.open(input_path)
        # 转换为RGB模式（避免透明通道问题）
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 计算原图比例和目标比例
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        # 按比例缩放（保证完整显示，不拉伸变形）
        if img_ratio > target_ratio:
            # 原图更宽，按高度缩放
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # 原图更高，按宽度缩放
            new_width = target_width
            new_height = int(new_width / img_ratio)
        
        # 缩放图片
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 裁剪到目标尺寸（居中裁剪）
        left = (new_width - target_width) / 2
        top = (new_height - target_height) / 2
        right = left + target_width
        bottom = top + target_height
        final_img = resized_img.crop((left, top, right, bottom))
        
        # 保存图片（指定DPI）
        final_img.save(output_path, dpi=(dpi, dpi))
        print(f"✅ 1寸照片已生成：{output_path}")
        print(f"📏 尺寸：{target_width}×{target_height}像素（{inch1_width_cm}×{inch1_height_cm}厘米）")
    
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {input_path}")
    except Exception as e:
        print(f"❌ 处理失败：{str(e)}")

# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 替换为你的图片路径
    input_photo = "original_photo.jpg"  # 输入图片
    output_photo = "1inch_photo.jpg"    # 输出1寸照片
    resize_to_1inch_photo(input_photo, output_photo)

