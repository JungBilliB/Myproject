import streamlit as st
import openai
import os
from typing import Optional

# 페이지 설정
st.set_page_config(
    page_title="시니어 복지 혜택 상담 비서",
    page_icon="👵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS - 시니어 친화적 디자인
st.markdown("""
    <style>
    /* 전체 배경 연한 회색 */
    .stApp {
        background-color: #F5F5F5;
    }
    
    /* 제목 스타일 */
    h1 {
        font-size: 48px !important;
        font-weight: bold;
        color: #1a237e;
        text-align: center;
        margin-bottom: 30px;
    }
    
    h2 {
        font-size: 36px !important;
        font-weight: bold;
        color: #000000;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    h3 {
        font-size: 28px !important;
        font-weight: bold;
        color: #000000;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    /* 전체 텍스트 크기 */
    .stMarkdown, .stText {
        font-size: 22px !important;
        color: #000000;
        line-height: 1.8;
    }
    
    /* 텍스트 영역 스타일 */
    .stTextArea > div > div > textarea {
        font-size: 22px !important;
        line-height: 1.8;
        padding: 15px !important;
        border: 3px solid #2196F3 !important;
        border-radius: 10px !important;
    }
    
    .stTextArea label {
        font-size: 24px !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        font-size: 24px !important;
        padding: 20px 40px !important;
        width: 100%;
        background-color: #2196F3;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #1976D2;
    }
    
    /* 답변 박스 */
    .answer-box {
        background-color: #E3F2FD;
        padding: 35px;
        border-radius: 15px;
        border: 4px solid #2196F3;
        margin: 30px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .answer-box p {
        font-size: 22px !important;
        color: #000000;
        line-height: 2;
        margin: 10px 0;
    }
    
    /* 면책 문구 */
    .disclaimer-box {
        background-color: #FFF3E0;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
        margin-top: 30px;
    }
    
    .disclaimer-box p {
        font-size: 20px !important;
        color: #E65100;
        margin: 0;
        font-weight: 500;
    }
    
    /* 안내 박스 */
    .info-box {
        background-color: #E8F5E9;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 30px;
    }
    
    .info-box p {
        font-size: 20px !important;
        color: #000000;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# 복지 지침 요약본 (Knowledge Base)
WELFARE_GUIDELINES = """
# 복지 지침 요약본 (2025-26 기준)

## 1. 기초연금
- 대상: 만 65세 이상 한국 국적 어르신 중 소득인정액이 하위 70%인 분
- 2024년 선정기준액: 
  * 단독가구: 2,130,000원 이하
  * 부부가구: 3,408,000원 이하
- 신청: 관할 읍면동 주민센터 또는 국민연금공단
- 혜택: 월 지급액은 소득인정액에 따라 차등 지급

## 2. 노인장기요양보험
- 대상: 
  * 65세 이상 어르신
  * 65세 미만 중 노인성 질병(치매, 뇌혈관성 질환 등)을 가진 자
- 등급: 1~5급, 인지지원등급
- 혜택: 등급에 따라 다음 서비스 지원
  * 방문요양: 요양보호사가 가정을 방문하여 신체활동 지원, 일상생활 지원
  * 주야간보호: 낮 시간 동안 시설에서 보호 및 활동 지원
  * 요양시설: 장기요양시설 입소 지원
  * 단기보호: 일시적으로 시설에서 보호
- 신청: 관할 읍면동 주민센터 또는 국민건강보험공단
- 절차: 요양등급 판정 신청 → 등급 판정 → 서비스 이용

## 3. 긴급복지지원
- 대상: 위기 상황으로 생계가 곤란한 저소득층
- 위기 상황 예시:
  * 주소득자 사망, 실직, 폐업
  * 중한 질병 또는 부상
  * 가구원의 생명을 위협하는 가정폭력
  * 가구원의 행방불명 또는 구금
  * 화재, 자연재해 등으로 거주할 주거 상실
  * 그 밖에 긴급한 생계지원이 필요한 경우
- 신청: 관할 읍면동 주민센터
- 혜택: 생계비, 의료비, 주거비, 교육비 등 긴급 지원
"""

def get_welfare_consultation(user_situation: str) -> Optional[str]:
    """
    오픈라우터 API를 사용하여 복지 혜택 상담을 제공합니다.
    """
    # 오픈라우터 API 키 확인
    api_key = None
    try:
        if hasattr(st, 'secrets') and "OPENROUTER_API_KEY" in st.secrets:
            api_key = st.secrets["OPENROUTER_API_KEY"]
    except:
        pass
    
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        st.error("⚠️ OPENROUTER_API_KEY가 설정되지 않았습니다.")
        st.info("오픈라우터 API 키를 .streamlit/secrets.toml 파일에 설정해주세요.")
        return None
    
    # 오픈라우터는 OpenAI 호환 API를 제공합니다
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    system_prompt = f"""당신은 시니어 복지 전문 상담사입니다. 아래의 복지 지침을 바탕으로 사용자의 상황에 맞는 복지 혜택을 안내해주세요.

{WELFARE_GUIDELINES}

[상담 가이드라인]
1. 사용자가 제공한 정보(나이, 가구원수, 경제 상황, 건강 상태 등)를 바탕으로 적합한 복지 혜택을 추천해주세요.
2. 각 복지 혜택의 신청 방법과 필요한 서류를 친절하게 설명해주세요.
3. 사용자의 상황에 맞는 구체적인 조언을 제공해주세요.
4. 답변은 친절하고 이해하기 쉽게 작성해주세요.
5. 복지 혜택이 여러 개 해당될 수 있으므로 모두 안내해주세요.

[답변 형식]
- 사용자 상황 분석
- 추천 복지 혜택 (각 항목별로 명확히 구분)
- 신청 방법 및 필요 서류
- 추가 안내사항"""

    user_prompt = f"""다음은 상담을 요청하는 어르신의 상황입니다:

{user_situation}

위 상황에 맞는 복지 혜택을 안내해주세요."""

    # 사용 가능한 모델 목록 (우선순위 순)
    models = [
        "xiaomi/mimo-v2-flash:free",
        "nvidia/nemotron-3-nano-30b-a3b:free",
        "mistralai/devstral-2512:free",
        "qwen/qwen3-coder:free"
    ]
    
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # 첫 번째 모델이 실패하면 다음 모델 시도
            if model == models[-1]:
                # 마지막 모델까지 모두 실패한 경우
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                st.info("💡 모든 모델이 사용 불가능합니다. 잠시 후 다시 시도해주세요.")
                return None
            continue
    
    return None

def main():
    st.title("👵 시니어 복지 혜택 상담 비서")
    
    # 안내 문구
    st.markdown("""
    <div class="info-box">
        <p><strong>안내:</strong> 나이, 가구원수, 경제 상황, 건강 상태 등을 자유롭게 입력해주세요.<br>
        AI가 복지 지침을 분석하여 적합한 복지 혜택과 신청 방법을 안내해드립니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 입력 섹션
    st.markdown("### 📝 상황 입력")
    
    user_situation = st.text_area(
        "상황을 입력해주세요:",
        placeholder="예: 저는 68세이고 혼자 살고 있습니다. 월 소득이 약 150만원 정도이고, 최근에 치매 진단을 받았습니다. 어떤 복지 혜택을 받을 수 있을까요?",
        height=200,
        label_visibility="visible",
        key="situation_input"
    )
    
    # 상담 요청 버튼
    if st.button("복지 혜택 상담받기", type="primary", use_container_width=True, key="consult_button"):
        if user_situation and user_situation.strip():
            with st.spinner("복지 혜택을 분석하고 있습니다... 잠시만 기다려주세요."):
                result = get_welfare_consultation(user_situation.strip())
                
                if result:
                    st.markdown("---")
                    st.markdown("### 💡 복지 혜택 안내")
                    st.markdown(f'<div class="answer-box">{result}</div>', unsafe_allow_html=True)
                    
                    # 면책 문구
                    st.markdown("""
                    <div class="disclaimer-box">
                        <p>⚠️ <strong>면책 문구:</strong> 이 결과는 참고용이며 정확한 판정은 관할 읍면동 주민센터 문의가 필요합니다.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("상담 생성에 실패했습니다. API 키를 확인해주세요.")
        else:
            st.warning("⚠️ 상황을 입력해주세요.")
    
    # 하단 안내
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 18px; margin-top: 40px;">
        <p>💡 복지 혜택 신청은 관할 읍면동 주민센터에서 직접 문의하시기 바랍니다.</p>
        <p style="margin-top: 10px;">📞 문의: 관할 읍면동 주민센터 또는 복지상담전화 129</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
