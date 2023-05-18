import streamlit as st
st.markdown('# Azure PDF Books')
st.markdown('### 演示 Azure Open AI LangChain 多 PDF 的嵌入和詢問')
st.markdown('----')

# 測試環境使用 AZURE_OPENAI_API_KEY 設定在 Streamlit 後臺。
import os
if os.getenv("AZURE_OPENAI_API_KEY") is not None:
    st.session_state['AZURE_OPENAI_API_KEY'] = os.getenv("AZURE_OPENAI_API_KEY")

# 輸入 AZURE_OPENAI_API_KEY  
if 'AZURE_OPENAI_API_KEY' not in st.session_state or st.session_state['AZURE_OPENAI_API_KEY'] == "": 
    inputkey = st.text_input("請輸入您的 AZURE OPENAI_API_KEY：例如39............................bb")           
    st.session_state['AZURE_OPENAI_API_KEY'] = inputkey

if st.session_state['AZURE_OPENAI_API_KEY'] != "":
    st.write('您的輸入的 AZURE OPENAI_API_KEY：', st.session_state['AZURE_OPENAI_API_KEY']) 
    st.write('您可以開始使用本網頁的功能了。')
    st.write('如果要重新輸入，請按 F5 重新整理網頁。')