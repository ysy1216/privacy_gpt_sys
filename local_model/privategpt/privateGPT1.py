#!/usr/bin/env python3
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All, LlamaCpp
import os
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

load_dotenv()
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')
model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH', 8))
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))


def ask(query):
    loader = TextLoader("local_model/privategpt/source_documents/chat.txt", "utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    docsearch = Chroma.from_documents(texts, embeddings)
    callbacks = []
    llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', n_batch=model_n_batch,
                  callbacks=callbacks, verbose=False, n_threads=8)
    from langchain.prompts import PromptTemplate
    myTemplate = '''使用以下上下文来回答最后的问题。
        {context}
        查找与{question}相似度最高的句子，将{question}中的*去除并直接将去除*号后的句子回答
        '''
    PROMPT = PromptTemplate(input_variables=["context", "question"], template=myTemplate)
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(),
                                     chain_type_kwargs=chain_type_kwargs,  return_source_documents=True)
    result = qa({"query": query})
    print(result)
    return result