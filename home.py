import streamlit as st
st.markdown('# DEMO')
st.markdown('# Azure openAI langchain PDF')
st.markdown('----')
st.markdown('## 這裏可以演示 langchain PDF 的編碼和查詢')

# 測試環境使用 AZURE_OPENAI_API_KEY 設定在 Streamlit 後臺。
# import os
# if os.getenv("AZURE_OPENAI_API_KEY") is not None:
#     st.session_state['AZURE_OPENAI_API_KEY'] = os.getenv("AZURE_OPENAI_API_KEY")

# 輸入 AZURE_OPENAI_API_KEY  
if 'AZURE_OPENAI_API_KEY' not in st.session_state or st.session_state['AZURE_OPENAI_API_KEY'] == "": 
    inputkey = st.text_input("請輸入您的 AZURE OPENAI_API_KEY：例如xx39d931157d574944954f02a48c6567xx")           
    st.session_state['AZURE_OPENAI_API_KEY'] = inputkey

if st.session_state['AZURE_OPENAI_API_KEY'] != "":
    st.write('您的輸入的 AZURE OPENAI_API_KEY：', st.session_state['AZURE_OPENAI_API_KEY']) 
    st.write('如果要重新輸入，請按 F5 重新整理網頁。')