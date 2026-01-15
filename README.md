# 시니어 복지 혜택 상담 비서

시니어를 위한 복지 혜택 상담을 제공하는 Streamlit 애플리케이션입니다.

## 기능

- 사용자의 상황(나이, 가구원수, 경제 상황, 건강 상태 등)을 입력받아 적합한 복지 혜택 안내
- 기초연금, 노인장기요양보험, 긴급복지지원 등 복지 혜택 정보 제공
- AI 기반 맞춤형 상담 서비스
- 시니어 친화적 큰 글씨 UI

## 설치 및 실행

### 로컬 실행

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. API 키 설정:
`.streamlit/secrets.toml` 파일을 생성하고 다음 내용을 추가하세요:
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

3. 앱 실행:
```bash
streamlit run app.py
```

## Streamlit Cloud 배포

1. GitHub 저장소에 코드 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud)에 접속하여 로그인
3. "New app" 클릭
4. GitHub 저장소 선택
5. Main file path: `app.py` 설정
6. Secrets에 `OPENROUTER_API_KEY` 추가
7. Deploy 클릭

## 사용 모델

다음 무료 모델을 순차적으로 시도합니다:
- xiaomi/mimo-v2-flash:free
- nvidia/nemotron-3-nano-30b-a3b:free
- mistralai/devstral-2512:free
- qwen/qwen3-coder:free

## 면책 문구

이 결과는 참고용이며 정확한 판정은 관할 읍면동 주민센터 문의가 필요합니다.
