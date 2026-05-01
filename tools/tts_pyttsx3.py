import argparse
import datetime
import os
import pyttsx3


def text_to_speech_offline(text, output_file="output.mp3"):
    engine = pyttsx3.init()

    # 可选：设置语速和音量
    rate = engine.getProperty("rate")
    engine.setProperty("rate", max(50, rate - 50))
    print(f"当前语速: {rate}")

    volume = engine.getProperty("volume")
    engine.setProperty("volume", 0.8)
    print(f"当前音量: {volume}")

    engine.save_to_file(text, output_file)
    engine.runAndWait()
    print(f"音频已保存至: {output_file}")


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
    return parser.parse_args()


def _default_filename() -> str:
    now = datetime.datetime.now()
    return now.strftime("TTS%Y%m%d-%H%M%S.mp3")


def resolve_output_path(output_path: str | None) -> str:
    home_dir = os.path.expanduser("~")
    music_dir = os.path.join(home_dir, "Music")
    os.makedirs(music_dir, exist_ok=True)

    if not output_path:
        return os.path.join(music_dir, _default_filename())

    output_path = os.path.expanduser(output_path)
    dir_name = os.path.dirname(output_path)
    base_name = os.path.basename(output_path)

    if dir_name and not base_name:
        output_file = os.path.join(os.path.abspath(dir_name), _default_filename())
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        return output_file

    if dir_name:
        output_file = os.path.abspath(output_path)
    else:
        output_file = os.path.join(music_dir, output_path)

    if not os.path.basename(output_file):
        output_file = os.path.join(os.path.dirname(output_file), _default_filename())

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    return output_file


if __name__ == "__main__":
    args = parse_args()
    output_file = resolve_output_path(args.output)
    text_to_speech_offline(args.text, output_file)
