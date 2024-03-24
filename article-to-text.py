





"""
loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()

    # Split and embed the text in the documents
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()

    # Store the embeddings in a database as local files
    db = FAISS.from_documents(texts, embeddings)
    db.save_local('vectorstore/db_faiss')
    retriever = db.as_retriever()
"""

# certificates, AWS, cloud, internships, connections 