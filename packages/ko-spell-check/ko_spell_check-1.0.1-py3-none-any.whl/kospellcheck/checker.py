# spell_checker/checker.py

import requests
import re


class SpellChecker:
    def __init__(self, passport_key: str = None):
        self.base_url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"
        self.passport_key_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=%EB%A7%9E%EC%B6%94&qdt=0&ie=utf8&query=%EB%A7%9E%EC%B6%A4%EB%B2%95%EA%B2%80%EC%82%AC%EA%B8%B0"
        self.passport_key = passport_key or self.extract_passport_key()

    def check_spelling(self, text: str):
        if not self.passport_key:
            return {"error": "passportKey를 가져오지 못했습니다."}

        params = {
            "passportKey": self.passport_key,
            "_callback": "jQuery11240248871280810548_1736152095925",
            "q": text,
            "where": "nexearch",
            "color_blindness": 0,
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"HTTP 요청 실패: {e}"}

        match = re.search(r"jQuery\d+_\d+\((.*)\);", response.text)
        if not match:
            self.passport_key = self.extract_passport_key()
            if self.passport_key:
                return self.check_spelling(text)
            return {"error": "응답 형식이 올바르지 않습니다."}

        data = match.group(1)
        try:
            result = eval(data)
            message = result["message"]["result"]
            return {
                "original_text": text,
                "corrected_text": message["notag_html"],
                "error_count": message["errata_count"],
            }
        except (KeyError, ValueError) as e:
            self.passport_key = self.extract_passport_key()
            if self.passport_key:
                return self.check_spelling(text)
            return {"error": f"응답 처리 중 오류 발생: {e}"}

    def clean_text_and_check(self, text: str):
        cleaned_text = re.sub(r"[^\w\sㄱ-ㅎㅏ-ㅣ가-힣]", "", text)
        return self.check_spelling(cleaned_text)

    def extract_passport_key(self):
        try:
            response = requests.get(self.passport_key_url)
            response.raise_for_status()
            html_content = response.text
            match = re.search(r'passportKey=([a-f0-9]+)', html_content)
            return match.group(1) if match else None
        except requests.exceptions.RequestException:
            return None
