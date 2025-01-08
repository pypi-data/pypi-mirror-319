


# ko-spell-check  

`ko-spell-check`는 네이버 맞춤법 검사 API를 활용하여 한국어 텍스트의 맞춤법 오류를 검사하고 교정된 텍스트를 제공하는 Python 패키지입니다.  

---  
## 📦 설치  Python 3.7 이상 버전에서 사용 가능합니다.  

```
pip install ko-spell-check
```


* * *

🚀 주요 기능
--------

1.  **맞춤법 검사**: 입력한 문장의 맞춤법 오류를 교정하고 교정된 결과를 반환합니다.
2.  **특수문자 제거 후 검사**: 텍스트에서 특수문자를 제거한 뒤 맞춤법 검사를 수행합니다.
3.  **자동 passportKey 갱신**: 유효하지 않은 passportKey가 제공된 경우, 자동으로 최신 값을 가져옵니다.

* * *

🔨 사용법
------

### 1\. **기본 맞춤법 검사**

```
from kospellcheck import SpellChecker  
# SpellChecker 초기화 (passport_key는 네이버 API 키). 
spell_checker = SpellChecker("your_passport_key") # your_passport_key 없으면 SpellChecker() 로 사용

# 맞춤법 검사 수행 
result = spell_checker.check_spelling("맞춤법 검사할 문장") 
print(result)
```

**출력 예시**:

```
{     
    "original_text": "맞춤법 검사할 문장",     
    "corrected_text": "맞춤법 검사한한 문장",     
    "error_count": 0 
}
```

* * *

### 2\. **특수문자 제거 후 맞춤법 검사**


```
from kospellcheck import SpellChecker  
spell_checker = SpellChecker("your_passport_key")  # 특수문자를 제거한 후 맞춤법 검사 your_passport_key 없으면 SpellChecker() 로 사용
result = spell_checker.clean_text_and_check("맞춤법 검사할 문장!!!") 
print(result)
```

**출력 예시**:

```
{
    "original_text": "맞춤법 검사할 문장!!!",
    "corrected_text": "맞춤법 검사한 문장",
    "error_count": 0 
}
```

* * *

### 3\. **passportKey 자동 갱신**

`passportKey`가 만료되었거나 올바르지 않을 경우, 자동으로 갱신하여 재시도합니다.

* * *

📋 반환 값 설명
----------

`check_spelling`과 `clean_text_and_check` 메서드는 다음과 같은 정보를 포함한 딕셔너리를 반환합니다:

|Key|설명|타입|
|------|---|---|
|original_text|사용자가 입력한 원본 텍스트|str|
|corrected_text|교정된 텍스트|str|
|error_count|발견된 맞춤법 오류 개수|int|
|error(optional)|에러 발생 시 에러 메시지|str|


* * *

🧪 테스트
------

`ko-spell-check`에는 간단한 테스트 코드가 포함되어 있습니다. 테스트를 실행하려면 다음 명령어를 사용하세요:

`python -m unittest discover tests`

* * *

🤝 기여
-----

`ko-spell-check`는 오픈 소스 프로젝트로, 누구나 기여할 수 있습니다.

### 기여 방법

1.  이 저장소를 포크합니다.
2.  새로운 브랜치를 생성합니다. (`git checkout -b feature/기능추가`)
3.  변경 사항을 커밋합니다. (`git commit -m 'Add 새로운 기능'`)
4.  브랜치를 푸시합니다. (`git push origin feature/기능추가`)
5.  Pull Request를 생성합니다.

* * *

📄 라이선스
-------

이 프로젝트는 MIT 라이선스 하에 배포됩니다. LICENSE 파일을 참조하세요.

* * *

🔗 참고
-----

*   네이버 맞춤법 검사 API
*   [PyPI - ko\-spell\-check](https://pypi.org/project/ko-spell-check/)

* * *

👩‍💻 개발자 정보
------------

*   **개발자**: [김형진](https://github.com/gudwls215)
*   **문의**: gudwls215@github.com
