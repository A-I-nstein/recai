#####-----importing neccessary libraries-----#####

import time
import streamlit as st
import model

#####-----Backend Elements-----#####

def get_rel_fun(case_summary):
    statutes, case_docs = model.predict(case_summary)
    return statutes, case_docs

#####-----UI Elements-----#####

st.set_page_config(layout="wide")

hide_streamlit_style = """
                   <style>
                   #MainMenu {visibility: hidden;}
                   footer {visibility: hidden;}
                   </style>
                   """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.markdown('<h1 style = "color:#66bfbf; font-size: 75px; text-align:center; font-weight:bold">RECAi</h1>', unsafe_allow_html=True)
st.markdown('<h2 style = "color:#f76b8a; text-align: center;">Cognitive Intelligence for Legal Assistance', unsafe_allow_html=True)
st.text("")
st.markdown('<h4 style = "text-align: justify;">Cognitive Intelligence for Legal Assistance aims at solving legal informatics problems. Given a legal scenario the cognitive system retrieves related precedents and statutes. The cognitive model would help advocates and magistrates by reducing the time spent on legal research for finding the related court case precedents and legal statutes, thereby reducing the duration of the  process of jurisdiction.', unsafe_allow_html=True)

st.text("")
st.text("")

st.subheader("Type the case summary here!")
case_summary = st.text_area("", height=250)

st.text("")

predict = st.button("Find relevant legal documents")

st.text("")

progress_bar = st.progress(0)

col1, col2 = st.columns(2)

st.text("")

statutes_container = col1.container()

st.text("")

document_container = col2.container()

#####-----Button function-----#####

if predict:
    if len(case_summary) <= 0:
        st.error('Please enter some text...')
    else:
        statutes, case_docs = get_rel_fun(case_summary)

        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.001)

        with statutes_container:

            st.subheader("Relevant Statutes")
            for i in statutes:
                with st.expander(i):
                    st.write(statutes[i])

        with document_container:

            st.subheader("Relevant Case Documents")
            for i in case_docs:
                with st.expander(i):
                    st.write(case_docs[i])
