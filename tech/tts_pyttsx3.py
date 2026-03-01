import pyttsx3


def text_to_speech_offline(text, output_file="output.mp3"):
    engine = pyttsx3.init(
        debug=True,
    )

    # 可选：设置语速和音量
    rate = engine.getProperty("rate")
    engine.setProperty("rate", rate - 50)
    print(f"当前语速: {rate}")

    volume = engine.getProperty("volume")
    engine.setProperty("volume", 0.8)
    print(f"当前音量: {volume}")

    voice = engine.getProperty("voice")
    print(f"当前语音: {voice})")

    # 语音列表
    voices = engine.getProperty("voices")
    for i, voice in enumerate(voices):
        print(f"索引 {i}: {voice.name} ({voice.id})")
    # engine.setProperty("voice", voices[1].id)

    # 播放音频
    engine.say(text)

    # 存储文件
    # engine.save_to_file(text, output_file)

    engine.runAndWait()
    print(f"音频已保存至: {output_file}")


# 文本转音频
# text_to_speech_offline("LangChain 你好，我来了！", "data/pyttsx3.mp3")
# text_to_speech_offline("野火烧不尽，春风吹又生！", "data/pyttsx3.mp3")
# text_to_speech_offline("What a nice day.", "data/pyttsx3.mp3")
text_to_speech_offline(
    "而这个config.py我存放在上级目录中，即项目根目录：D:\\CodeSpace\\me-agent\\",
    "data/pyttsx3.mp3",
)
