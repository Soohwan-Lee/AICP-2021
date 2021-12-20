import requests

# 자신의 REST_API_KEY를 입력하세요!
REST_API_KEY = "48995414c941eef20bfff6ad9c023947"


class KakaoTTS:

	def __init__(self, text, API_KEY=REST_API_KEY):
		self.resp = requests.post(
			url="https://kakaoi-newtone-openapi.kakao.com/v1/synthesize",
			headers={
				"Content-Type": "application/xml",
				"Authorization": f"KakaoAK {API_KEY}"
			},
			data=f"<speak>{text}</speak>".encode('utf-8')
		)

	def save(self, filename="output.mp3"):
		with open(filename, "wb") as file:
			file.write(self.resp.content)


if __name__ == '__main__':
    text = """
    <prosody rate="fast" volume="loud">
    <voice name="WOMAN_DIALOG_BRIGHT">
    저는 공학관 백사동 구백칠 다시 에이호에서 태어났습니다.
    </voice>
    </prosody>
    """
    tts = KakaoTTS(text)
    tts.save("./born.mp3")
