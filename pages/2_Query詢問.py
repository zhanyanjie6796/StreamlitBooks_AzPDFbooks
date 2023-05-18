import streamlit as st
# import tempfile
# from PyPDF2 import PdfReader

def style_func():
    st.write('風格化處理')

def main():
    # AZURE_OPENAI_API_KEY  
    if 'AZURE_OPENAI_API_KEY' not in st.session_state or st.session_state['AZURE_OPENAI_API_KEY'] == "":        
        st.markdown("###### 請回到首頁 home 輸入您的 AZURE OPENAI_API_KEY 再回來。")
        import sys # st.write('== 中斷測試 ==')
        sys.exit('== 中斷測試 ==')
    else:
        # st.write('您的 AZURE OPENAI_API_KEY：', st.session_state['AZURE_OPENAI_API_KEY'])  
        st.markdown("## Query 詢問")
    
    st.write('這裏的查詢資料以 docs1_AI 中的 PDF 檔案之向量索引爲例。')
    title  = st.text_input("###### 請輸入您要詢問的問題，例如：人工智慧的應用場景分成四大面向,台灣式繁體中文回答。")

    if title == "":
        import sys # st.write('== 中斷測試 ==')
        sys.exit('== 中斷測試 ==')
    # st.write('您的問題：', title)
    st.markdown("###### 使用模型：gpt-35-turbo 為您分析中 。。。。。。")

    import os
    # from dotenv import load_dotenv

    # Load environment variables (set OPENAI_API_KEY and OPENAI_API_BASE in .env)
    # load_dotenv()
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
    os.environ["OPENAI_API_BASE"] = "https://user1-create-gpt.openai.azure.com/" # 修改成自己的 API_BASE。 
    os.environ["OPENAI_API_KEY"] = st.session_state['AZURE_OPENAI_API_KEY']
    # os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY") # 修改成自己的 API_KEY。例如："39............................bb"
    # st.write("demo："+os.environ["OPENAI_API_KEY"]) # 設定在 streamlit 網站的 Secrets 的環境變數中。

    pdf_path =  "docs1_AI"
    # pdf_path =  "docs2_Buddhism"
    # pdf_path =  "docs3_merge_AI_Buddhism"
    data_store = pdf_path + "/data_store" 

    from langchain.embeddings.openai import OpenAIEmbeddings

    # 開始測量轉換時間
    import time    
    start = time.time() 

    # vector load start  ===========================================================================

    # To load the Vector Store from files:
    # Create datastore
    from langchain.vectorstores import FAISS
    if os.path.exists(data_store):
        vector_store = FAISS.load_local(data_store,OpenAIEmbeddings())
    else:
        # print(f"Missing files. Upload index.faiss and index.pkl files to data_store directory first")
        st.write("Missing files. Upload index.faiss and index.pkl files to data_store directory first")
    
    # Query using the vector store
    # Set up the chat model and specific prompt

    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    system_template="""Use the following pieces of context to answer the users question.
    Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
    If you don't know the answer, just say that "I don't know", don't try to make up an answer.
    ----------------
    {summaries}"""
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)    

    # models 下面這些都可以用。
    #彥杰修改AzureOpenAI # Initialize gpt-35-turbo and our embedding model
    # from langchain.llms import AzureOpenAI
    # llm = AzureOpenAI(deployment_name="text-davinci-003", model_name="text-davinci-003", temperature=0.5, max_tokens=500) # OK這個比較正常。

    # models 使用 "gpt-4" 查詢等待時間會比較久。
    from langchain.chat_models import AzureChatOpenAI 
    llm = AzureChatOpenAI(deployment_name="gpt-35-turbo", model_name="gpt-35-turbo", temperature=0.5, max_tokens=500) 
    # llm = AzureChatOpenAI(deployment_name="gpt-4", model_name="gpt-4", temperature=0.5, max_tokens=500) 
    # llm = AzureChatOpenAI(deployment_name="gpt-4-32k", model_name="gpt-4-32k", temperature=0.5, max_tokens=500)
   
    from langchain.chains import RetrievalQAWithSourcesChain
    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs
    )


    # st.write("===================================================")
    query = title
    ## Use the chain to query
    # query = "文章標題，台灣式繁體中文回答。"
    # query = "What is the author's name?"
    # query = "人工智慧的應用場景分成四大面向,台灣式繁體中文回答。"
    # query = "專家系統是什麽,台灣式繁體中文回答。"
    # query = "人工智慧是什麼.pdf的作者,台灣式繁體中文回答。"
    # query = "智慧,台灣式繁體中文回答。"
    result = chain(query)
    # print(result)
    # print(result,file=open('demo.txt', 'w',encoding='UTF-8'))

    # st.write("===================================================")
    # Print Answer
    # st.write("你的問題是："+result['question'])
    st.markdown("###### 你的問題是："+result['question'])
    st.write("答案是："+result['answer'])
    st.markdown('----')
    
    # Print Sources
    source_documents = result['source_documents']
    for index, document in enumerate(source_documents):
        # txt = st.text_area("文獻來源：", "哈哈哈\n你好")         
        st.text_area("###### Source"+str(index + 1)+"&nbsp;&nbsp;&nbsp;&nbsp;檔名："+
                     document.metadata['source']+"&nbsp;&nbsp;&nbsp;&nbsp;頁碼："+
                     str(document.metadata['page']+1), 
                     document.page_content,height=150)
        # 下面是原本的程式
        # st.write(f"\n\nSource {index + 1}:")
        # st.write("檔名："+document.metadata['source']+"    頁碼："+str(document.metadata['page']+1))    
        # st.write(f"  Page Content: {document.page_content}")

    # st.write("==============================================================")

    # 結束測量轉換時間
    end = time.time()
    st.markdown("###### query 執行時間：%f 秒" % (end - start))
    # st.write("query 執行時間：%f 秒" % (end - start))     
    # st.write("==== end =====================================================")   
   
    # import sys # st.write('== 中斷測試 ==')
    # sys.exit('== 中斷測試 ==')

    
if __name__ == "__main__":
    main()