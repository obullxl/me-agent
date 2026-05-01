# 工具列表

该目录包含常用实用脚本，当前支持 PDF 转图片和离线文本转语音两类工具。

## 工具说明

| 文件 | 功能说明 |
| --- | --- |
| [pdf_2_png.py](./pdf_2_png.py) | PDF 转 PNG：单个文件或目录批量转换 |
| [tts_pyttsx3.py](./tts_pyttsx3.py) | 离线文本转语音：支持 MP3/AIFF 输出，自定义语速音量 |

## 快速开始

1. 安装依赖：

```bash
pip install pymupdf pyttsx3
# macOS 用户额外安装: brew install ffmpeg
```

2. 进入工具目录：

```bash
cd ./me-agent/tools
```

3. 运行工具：

```bash
# PDF 转换
python pdf_2_png.py your_file.pdf

# 文本转语音
python tts_pyttsx3.py -t "Hello World"
```

## PDF 转 PNG

`pdf_2_png.py` 用于将单个 PDF 文件或 PDF 目录批量转换为 PNG 图片。

### 依赖

```bash
pip install pymupdf
```

### 示例

- 单个文件转换：

```bash
python pdf_2_png.py <PDF文件路径>
```

- 目录批量转换：

```bash
python pdf_2_png.py <PDF文件目录>
```

## TTS 语音合成工具

`tts_pyttsx3.py` 用于离线将文本转换为音频文件，支持 MP3 和 AIFF 格式。

### 依赖

```bash
pip install pyttsx3
```

**注意**：macOS 用户需要安装 `ffmpeg` 用于音频格式转换：

```bash
brew install ffmpeg  # macOS
# 或其他平台的包管理器
```

### 参数说明

| 参数 | 必需 | 说明 |
| --- | --- | --- |
| `-t, --text` | 是 | 要转换的文本内容 |
| `-o, --output` | 否 | 输出音频文件路径 |
| `-r, --rate` | 否 | 语速 (整数，默认自动调整) |
| `-v, --volume` | 否 | 音量 (0.0-1.0，默认 0.8) |

### 输出路径规则

- **未指定**：保存到 `~/Music/TTSYYYYMMDD-HHMMSS.mp3`
- **目录**：在指定目录生成 `TTSYYYYMMDD-HHMMSS.mp3`
- **文件名无扩展名**：自动添加 `.mp3` 扩展名
- **完整路径**：直接使用指定路径

### 支持格式

- `.mp3` (默认，推荐)
- `.aiff` (macOS 原生格式，无需转换)

### 示例

- 基本使用，默认保存：

```bash
python tts_pyttsx3.py -t "你好，世界"
```

- 指定输出文件：

```bash
python tts_pyttsx3.py -t "Hello World" -o result.mp3
```

- 指定目录（自动生成文件名）：

```bash
python tts_pyttsx3.py -t "测试" -o /tmp/
```

- 自定义语速和音量：

```bash
python tts_pyttsx3.py -t "自定义参数" -r 150 -v 0.9 -o output.mp3
```

- 输出 AIFF 格式：

```bash
python tts_pyttsx3.py -t "AIFF 格式" -o result.aiff
```

### 平台说明

- **macOS**：使用 NSSpeechSynthesizer，支持多种语言语音，MP3 输出需 ffmpeg 转换
- **Linux/Windows**：使用系统 TTS 引擎，直接支持 MP3 输出
- **默认保存路径**：`~/Music` (Linux/macOS) 或 `%USERPROFILE%\Music` (Windows)
