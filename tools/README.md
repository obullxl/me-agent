# 工具列表

该目录包含常用实用脚本，当前支持 PDF 转图片和离线文本转语音两类工具。

## 工具说明

| 文件 | 功能说明 |
| --- | --- |
| [pdf_2_png.py](./pdf_2_png.py) | 单个 PDF 转 PNG，或 PDF 目录批量转换为 PNG |
| [tts_pyttsx3.py](./tts_pyttsx3.py) | 离线文本转语音，生成音频文件 |

## 通用使用方式

1. 进入当前目录：

   ```bash
   cd ./me-agent/tools
   ```

2. 运行脚本：

   ```bash
   python <脚本名>.py [参数]
   ```

---

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

---

## TTS 语音合成工具

`tts_pyttsx3.py` 用于离线将文本转换为音频文件。

### 依赖

```bash
pip install pyttsx3
```

### 示例

- 仅指定文本，默认保存到系统用户目录 `Music` 目录，文件名自动生成：

```bash
python tts_pyttsx3.py -t "你好，世界"
```

- 指定输出文件名，默认目录为用户 `Music` 目录：

```bash
python tts_pyttsx3.py -t "你好，世界" -o result.mp3
```

- 指定完整路径：

```bash
python tts_pyttsx3.py -t "你好，世界" -o /tmp/result.mp3
```

- 指定目录但不指定文件名，生成时间戳文件名，例如 `TTS20260501-100345.mp3`：

```bash
python tts_pyttsx3.py -t "你好" -o /tmp/
```

### 默认保存路径

- Linux / macOS：默认保存到 `~/Music`
- Windows：默认保存到 `%USERPROFILE%\\Music`
