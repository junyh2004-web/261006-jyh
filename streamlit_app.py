from datetime import date

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Streamlit 요소 탐험실",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #18352d;
        --muted: #61736b;
        --leaf: #dcefe3;
        --coral: #ef765d;
    }
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { color: var(--ink); }
    [data-testid="stCaptionContainer"] { color: var(--muted); }
    .intro-band {
        padding: 1.4rem 1.6rem;
        margin: 0.3rem 0 1.3rem;
        border-left: 5px solid var(--coral);
        background: linear-gradient(105deg, #e8f3eb 0%, #f7f8f4 74%);
        border-radius: 4px;
    }
    .intro-band p { color: var(--muted); margin: 0.35rem 0 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Streamlit 요소 탐험실")
st.markdown(
    """
    <div class="intro-band">
      <strong>보고, 눌러 보고, 바로 확인해 보세요.</strong>
      <p>Streamlit은 Python 코드로 데이터 앱을 만드는 도구예요. 아래 탭에서 자주 쓰는 요소를 직접 조작해 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

overview = st.columns(3)
for column, label, value in zip(
    overview,
    ["화면 구성", "사용자 입력", "데이터 표현"],
    ["제목 · 설명", "버튼 · 위젯", "표 · 차트"],
):
    with column:
        st.metric(label=label, value=value)

basic_tab, input_tab, data_tab, layout_tab = st.tabs(
    ["기본 요소", "입력 위젯", "데이터와 차트", "레이아웃과 기타"]
)

with basic_tab:
    st.header("1. 화면에 내용을 보여 주기")
    st.write("`st.title`, `st.header`, `st.write`를 사용하면 화면에 제목과 설명을 배치할 수 있어요.")
    st.caption("작은 안내나 출처처럼 덜 강조할 내용은 캡션으로 표시합니다.")

    left, right = st.columns([1, 1])
    with left:
        st.subheader("버튼과 상태")
        st.write("버튼을 누를 때마다 횟수가 올라갑니다. 값은 세션 상태에 저장돼요.")
        if "click_count" not in st.session_state:
            st.session_state.click_count = 0
        if st.button("눌러 보기", icon="👆", key="counter_button"):
            st.session_state.click_count += 1
        st.metric("버튼을 누른 횟수", st.session_state.click_count)

    with right:
        st.subheader("상태 메시지")
        st.success("성공 메시지: 작업이 정상적으로 끝났을 때")
        st.info("정보 메시지: 참고할 내용을 알려줄 때")
        st.warning("주의 메시지: 확인이 필요한 상황을 알릴 때")

with input_tab:
    st.header("2. 입력 위젯 직접 조작하기")
    st.write("위젯은 사용자의 선택이나 값을 Python 변수로 전달합니다. 값을 바꾸면 페이지가 다시 실행돼 결과가 갱신돼요.")

    name = st.text_input("이름", placeholder="예: 민지")
    message = st.text_area("짧은 소개", placeholder="무엇을 만들고 싶은지 적어 보세요.", height=90)
    score = st.slider("만족도", min_value=0, max_value=100, value=65, step=5)

    choice_column, options_column = st.columns(2)
    with choice_column:
        favorite = st.selectbox("좋아하는 요소", ["차트", "표", "입력 폼", "지도"])
        pace = st.radio("학습 속도", ["천천히", "보통", "빠르게"], horizontal=True)
    with options_column:
        topics = st.multiselect(
            "관심 주제 (여러 개 선택 가능)",
            ["데이터 분석", "업무 자동화", "웹 앱", "인공지능"],
            default=["웹 앱"],
        )
        show_detail = st.checkbox("상세 결과도 보기", value=True)

    due_date = st.date_input("기억할 날짜", value=date.today())
    st.markdown("#### 입력 결과")
    st.write(f"안녕하세요, **{name or '처음 오신 분'}**! 선택한 요소는 **{favorite}**, 학습 속도는 **{pace}**예요.")
    st.progress(score, text=f"만족도 {score}%")
    if topics:
        st.write("관심 주제:", ", ".join(topics))
    else:
        st.write("관심 주제를 하나 이상 선택해 보세요.")
    if show_detail:
        st.info(f"기억할 날짜: {due_date:%Y년 %m월 %d일} · 소개: {message or '아직 입력하지 않았어요.'}")

    st.subheader("폼으로 한 번에 제출하기")
    st.write("폼 안의 값은 제출 버튼을 누를 때 한 번에 처리됩니다.")
    with st.form("feedback_form"):
        feedback = st.text_input("페이지에 대한 한마디", placeholder="예: 차트 예제가 유용해요")
        submitted = st.form_submit_button("의견 제출", type="primary")
    if submitted:
        if feedback.strip():
            st.success(f"의견을 확인했어요: {feedback}")
        else:
            st.warning("의견을 한 줄 입력해 주세요.")

with data_tab:
    st.header("3. 표를 고치고 차트로 살펴보기")
    st.write("`st.data_editor`는 표의 셀을 직접 수정할 수 있게 하고, 차트는 숫자의 변화를 한눈에 보여 줍니다.")

    monthly_data = pd.DataFrame(
        {
            "월": ["1월", "2월", "3월", "4월", "5월", "6월"],
            "방문자": [120, 155, 143, 190, 218, 205],
            "문의": [18, 22, 20, 31, 36, 34],
        }
    )
    edited_data = st.data_editor(
        monthly_data,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        key="monthly_data_editor",
    )

    chart_mode = st.radio("차트 종류", ["선 차트", "막대 차트"], horizontal=True)
    chart_data = edited_data.copy()
    for column_name in ["방문자", "문의"]:
        chart_data[column_name] = pd.to_numeric(chart_data[column_name], errors="coerce")
    chart_data = chart_data.dropna(subset=["월"]).set_index("월")
    chart_data = chart_data.dropna(axis="columns", how="all")

    if chart_data.empty or chart_data.select_dtypes(include="number").empty:
        st.info("표에 월과 숫자 데이터를 입력하면 차트가 나타납니다.")
    elif chart_mode == "선 차트":
        st.line_chart(chart_data)
    else:
        st.bar_chart(chart_data)

    st.caption("셀을 편집하거나 행을 추가·삭제하면 위 차트에도 바로 반영됩니다.")
    csv_data = edited_data.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "표를 CSV로 내려받기",
        data=csv_data,
        file_name="streamlit-demo.csv",
        mime="text/csv",
        icon="⬇️",
    )

with layout_tab:
    st.header("4. 화면을 나누고 내용을 정리하기")
    st.write("열, 탭, 접이식 영역을 사용하면 관련 내용을 묶어 화면을 읽기 쉽게 만들 수 있어요.")

    first_column, second_column = st.columns(2)
    with first_column:
        st.subheader("열")
        st.write("`st.columns`로 내용을 나란히 배치합니다.")
        st.metric("이번 주 방문", "1,284", "+12%")
    with second_column:
        st.subheader("토글과 숫자 입력")
        show_notice = st.toggle("알림 켜기", value=True)
        quantity = st.number_input("표시할 항목 수", min_value=1, max_value=20, value=5)
        if show_notice:
            st.info(f"항목 {quantity}개를 표시하도록 설정했어요.")
        else:
            st.caption("알림이 꺼져 있습니다.")

    with st.expander("접이식 설명 열기"):
        st.write("`st.expander`는 필요할 때만 펼쳐 보는 설명이나 추가 정보를 담습니다.")
        st.code('st.write("안녕하세요, Streamlit!")', language="python")

    st.subheader("진행 상태")
    progress_value = st.slider("진행률", min_value=0, max_value=100, value=40, key="layout_progress")
    st.progress(progress_value, text=f"진행률 {progress_value}%")

st.divider()
st.caption("이 페이지의 예제는 Streamlit 기본 기능과 이미 설치된 pandas만 사용합니다.")