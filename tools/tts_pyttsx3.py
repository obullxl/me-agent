import argparse
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import pyttsx3

SUPPORTED_EXTENSIONS = {".mp3", ".aiff"}


def get_extension_from_path(path: str) -> str:
    """从文件路径中提取扩展名，如果没有则返回空字符串。"""
    _, ext = os.path.splitext(path)
    return ext.lower()


def validate_output_path(output_path: str) -> None:
    """验证输出路径的扩展名是否支持。"""
    ext = get_extension_from_path(output_path)
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"不支持的音频格式: {ext}。支持的格式: {', '.join(SUPPORTED_EXTENSIONS)}")


def text_to_speech_offline(text: str, output_file: str = "output.mp3", rate: int | None = None, volume: float | None = None) -> None:
    """
    将文本转换为语音并保存为音频文件。

    Args:
        text: 要转换的文本
        output_file: 输出文件路径
        rate: 语速 (可选，默认使用引擎默认值调整)
        volume: 音量 (0.0-1.0，可选，默认 0.8)
    """
    try:
        engine = pyttsx3.init()
    except Exception as e:
        raise RuntimeError(f"初始化 TTS 引擎失败: {e}")

    # 设置语速
    if rate is not None:
        engine.setProperty("rate", rate)
        print(f"设置语速: {rate}")
    else:
        current_rate = engine.getProperty("rate")
        engine.setProperty("rate", max(50, current_rate - 50))
        print(f"当前语速: {current_rate}")

    # 设置音量
    if volume is not None:
        engine.setProperty("volume", volume)
        print(f"设置音量: {volume}")
    else:
        current_volume = engine.getProperty("volume")
        engine.setProperty("volume", 0.8)
        print(f"当前音量: {current_volume}")

    # macOS pyttsx3 只支持 .aiff，需要转换到其他格式
    if sys.platform == "darwin" and not output_file.lower().endswith(".aiff"):
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as temp_file:
            temp_aiff = temp_file.name

        try:
            engine.save_to_file(text, temp_aiff)
            engine.runAndWait()

            # 检查 ffmpeg 是否可用
            if not shutil.which("ffmpeg"):
                raise RuntimeError("ffmpeg 未安装，无法转换音频格式")

            result = subprocess.run(
                ["ffmpeg", "-i", temp_aiff, "-y", output_file],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"音频转换完成: {temp_aiff} -> {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"转换失败: {e.stderr}")
            raise RuntimeError(f"音频转换失败: {e}")
        finally:
            if os.path.exists(temp_aiff):
                os.remove(temp_aiff)
    else:
        engine.save_to_file(text, output_file)
        engine.runAndWait()

    print(f"音频已保存至: {output_file}")


def _default_filename(extension: str) -> str:
    """生成默认文件名，格式: TTSYYYYMMDD-HHMMSS{extension}"""
    now = datetime.datetime.now()
    return now.strftime(f"TTS%Y%m%d-%H%M%S{extension}")


def resolve_output_path(output_path: str | None) -> str:
    """
    解析输出路径。

    如果未指定路径，使用默认路径 ~/Music/TTSYYYYMMDD-HHMMSS.mp3
    如果指定目录但未指定文件名，添加默认文件名
    自动创建必要的目录
    """
    default_extension = ".mp3"
    home_dir = os.path.expanduser("~")
    music_dir = os.path.join(home_dir, "Music")
    os.makedirs(music_dir, exist_ok=True)

    if not output_path:
        return os.path.join(music_dir, _default_filename(default_extension))

    output_path = os.path.expanduser(output_path)
    dir_name = os.path.dirname(output_path)
    base_name = os.path.basename(output_path)

    if dir_name and not base_name:
        output_file = os.path.join(os.path.abspath(dir_name), _default_filename(default_extension))
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        return output_file

    if dir_name:
        output_file = os.path.abspath(output_path)
    else:
        output_file = os.path.join(music_dir, output_path)

    # 如果输出路径是一个现有目录，在其中创建默认文件名
    if os.path.isdir(output_file):
        output_file = os.path.join(output_file, _default_filename(default_extension))
    # 如果没有扩展名，添加默认扩展名
    elif not get_extension_from_path(output_file):
        output_file += default_extension

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    return output_file


def parse_args():
    parser = argparse.ArgumentParser(description="离线文本转语音并保存为音频文件")
    parser.add_argument("-t", "--text", type=str, required=True, help="要转换的文本内容")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="输出音频文件路径。如果未指定目录，则默认保存到系统 Music 目录；如果未指定文件名，则使用 TTSYYYYMMDD-HHMMSS.mp3",
    )
    parser.add_argument(
        "-r",
        "--rate",
        type=int,
        default=None,
        help="语速 (默认自动调整)",
    )
    parser.add_argument(
        "-v",
        "--volume",
        type=float,
        default=None,
        help="音量 (0.0-1.0，默认 0.8)",
    )
    return parser.parse_args()


"""
离线文本转语音工具

使用 pyttsx3 库将文本转换为语音并保存为音频文件。
在 macOS 上，由于 pyttsx3 只支持 AIFF 格式，会自动使用 ffmpeg 转换为其他格式。

支持的格式: MP3, AIFF

使用示例:
    python tts_pyttsx3.py -t "你好，世界"
    python tts_pyttsx3.py -t "Hello World" -o output.mp3 -r 150 -v 0.8
"""

import argparse
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import pyttsx3


if __name__ == "__main__":
    args = parse_args()
    output_file = resolve_output_path(args.output)
    validate_output_path(output_file)
    text_to_speech_offline(args.text, output_file, args.rate, args.volume)
