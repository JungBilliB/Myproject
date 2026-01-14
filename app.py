import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="시니어 혈압 관리 대시보드",
    page_icon="🩺",
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
        font-size: 42px !important;
        font-weight: bold;
        color: #000000;
        text-align: center;
        margin-bottom: 30px;
    }
    
    h2 {
        font-size: 32px !important;
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
    
    /* 입력 필드 스타일 */
    .stDateInput > div > div > input, .stNumberInput > div > div > input {
        font-size: 22px !important;
        padding: 15px !important;
    }
    
    .stDateInput label, .stNumberInput label {
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
    
    /* 상태 박스 */
    .status-box {
        padding: 40px;
        border-radius: 15px;
        margin: 30px 0;
        text-align: center;
        border: 5px solid;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .status-normal {
        background-color: #C8E6C9;
        border-color: #4CAF50;
        color: #1B5E20;
    }
    
    .status-warning {
        background-color: #FFF9C4;
        border-color: #FBC02D;
        color: #F57F17;
    }
    
    .status-high {
        background-color: #FFCDD2;
        border-color: #F44336;
        color: #B71C1C;
    }
    
    .status-text {
        font-size: 32px !important;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .status-value {
        font-size: 28px !important;
        margin: 10px 0;
    }
    
    /* 입력 섹션 */
    .input-section {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* 테이블 스타일 */
    .dataframe {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# session_state 초기화
if 'blood_pressure_data' not in st.session_state:
    st.session_state.blood_pressure_data = []

def add_blood_pressure_record(date, systolic, diastolic):
    """혈압 기록 추가"""
    st.session_state.blood_pressure_data.append({
        '날짜': date,
        '수축기 혈압': systolic,
        '이완기 혈압': diastolic
    })

def get_blood_pressure_status(systolic, diastolic):
    """혈압 상태 판정"""
    # 기준: 수축기/이완기
    # 정상: 수축기 < 120 and 이완기 < 80
    # 주의: (120 <= 수축기 < 140) or (80 <= 이완기 < 90)
    # 고혈압: 수축기 >= 140 or 이완기 >= 90
    
    if systolic < 120 and diastolic < 80:
        return "정상", "status-normal", "🟢"
    elif systolic < 140 and diastolic < 90:
        return "주의", "status-warning", "🟡"
    else:
        return "고혈압", "status-high", "🔴"

def main():
    st.title("🩺 시니어 혈압 관리 대시보드")
    
    # 안내 문구
    st.markdown("""
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin-bottom: 30px; border-left: 5px solid #2196F3;">
        <p style="font-size: 20px; color: #000000; margin: 0;">
        <strong>안내:</strong> 날짜와 혈압 수치를 입력하신 후 '기록 추가' 버튼을 눌러주세요.<br>
        입력된 데이터는 그래프와 표로 표시되며, 현재 혈압 상태를 확인할 수 있습니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 입력 섹션
    st.markdown("### 📝 혈압 기록 입력")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date = st.date_input(
            "날짜",
            value=datetime.now().date(),
            label_visibility="visible"
        )
    
    with col2:
        systolic = st.number_input(
            "수축기 혈압 (높은 수치)",
            min_value=0,
            max_value=300,
            value=120,
            step=1,
            label_visibility="visible"
        )
    
    with col3:
        diastolic = st.number_input(
            "이완기 혈압 (낮은 수치)",
            min_value=0,
            max_value=300,
            value=80,
            step=1,
            label_visibility="visible"
        )
    
    # 기록 추가 버튼
    if st.button("기록 추가", type="primary", use_container_width=True, key="add_button"):
        add_blood_pressure_record(date, systolic, diastolic)
        st.success(f"✅ {date} 혈압 기록이 추가되었습니다.")
        st.rerun()
    
    # 데이터가 있는 경우
    if st.session_state.blood_pressure_data:
        # 데이터프레임 생성
        df = pd.DataFrame(st.session_state.blood_pressure_data)
        df = df.sort_values('날짜').reset_index(drop=True)
        
        # 최근 기록 가져오기
        latest_record = df.iloc[-1]
        latest_systolic = latest_record['수축기 혈압']
        latest_diastolic = latest_record['이완기 혈압']
        
        # 혈압 상태 판정
        status_text, status_class, status_icon = get_blood_pressure_status(latest_systolic, latest_diastolic)
        
        st.markdown("---")
        
        # 현재 혈압 상태 표시
        st.markdown("### 📊 현재 혈압 상태")
        st.markdown(f"""
        <div class="status-box {status_class}">
            <div class="status-text">{status_icon} {status_text}</div>
            <div class="status-value">수축기: {latest_systolic} mmHg / 이완기: {latest_diastolic} mmHg</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 그래프 표시
        st.markdown("### 📈 혈압 변화 그래프")
        
        # 그래프용 데이터 준비
        df_melted = df.melt(
            id_vars='날짜',
            value_vars=['수축기 혈압', '이완기 혈압'],
            var_name='혈압 종류',
            value_name='혈압 수치'
        )
        
        # Plotly 그래프 생성
        fig = px.line(
            df,
            x='날짜',
            y=['수축기 혈압', '이완기 혈압'],
            title='날짜별 혈압 변화',
            labels={'value': '혈압 (mmHg)', '날짜': '날짜'},
            color_discrete_map={
                '수축기 혈압': '#D32F2F',
                '이완기 혈압': '#1976D2'
            }
        )
        
        fig.update_layout(
            font=dict(size=18),
            title_font=dict(size=24),
            height=500,
            xaxis_title="날짜",
            yaxis_title="혈압 (mmHg)",
            legend=dict(
                font=dict(size=20),
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # 동그라미 마커와 선으로 표시
        fig.update_traces(
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=12, line=dict(width=2, color='white'))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 데이터 테이블 표시
        st.markdown("### 📋 혈압 기록표")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # 데이터 삭제 기능 (선택사항)
        st.markdown("---")
        st.markdown("### 🗑️ 기록 삭제")
        
        if st.button("모든 기록 삭제", type="secondary", use_container_width=True, key="clear_button"):
            st.session_state.blood_pressure_data = []
            st.success("✅ 모든 기록이 삭제되었습니다.")
            st.rerun()
    else:
        # 데이터가 없을 때 안내
        st.info("💡 혈압 기록을 입력하면 그래프와 표가 표시됩니다.")
    
    # 하단 안내
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 18px; margin-top: 40px;">
        <p><strong>혈압 기준 안내:</strong><br>
        정상: 수축기 < 120 mmHg, 이완기 < 80 mmHg<br>
        주의: 수축기 120-139 mmHg 또는 이완기 80-89 mmHg<br>
        고혈압: 수축기 ≥ 140 mmHg 또는 이완기 ≥ 90 mmHg</p>
        <p style="margin-top: 20px;">💡 이 도구는 참고용입니다. 건강 상태 확인은 전문의와 상담하시기 바랍니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
