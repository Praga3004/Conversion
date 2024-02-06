import os
import tk
from tkinter import filedialog
import shutil
from os import listdir,getcwd
from os.path import isfile,join
from llama_index import set_global_service_context,VectorStoreIndex,ServiceContext,PromptHelper,SimpleDirectoryReader,OpenAIEmbedding,StorageContext,load_index_from_storage
from llama_index.llms import OpenAI
from llama_index.text_splitter import SentenceSplitter

llm = OpenAI(model="gpt-3.5-turbo",temperature=0,max_tokens=256)

emd=OpenAIEmbedding()
text_spilitter= SentenceSplitter(chunk_size=1024,chunk_overlap=20)
prompt_help=PromptHelper(
    context_window=4096,#How many precedding context of data are taken while providing response
    num_output=256,
    chunk_overlap_ratio=0.1,
    chunk_size_limit=None

)   
def select_file():
    path=filedialog.askopenfilename(title="Select the file")
    if path:
        dest_direc=getcwd()
        shutil.move(path,dest_direc)
        print(f"File {path} moved to {dest_direc}")

    

Vector_Store="Storage/"
newfile=False
file_dir=[f for f in listdir(getcwd()) if isfile(join(getcwd(),f)) ]
if os.path.exists("Files.txt"):
    with open("Files.txt","r") as f:
        content=[x for x in f.read()]
    
    for x in file_dir:
        if x not in content:
            newfile=True



if ((not os.path.exists(Vector_Store))or (newfile)):
    doc = SimpleDirectoryReader(r"F:\Projects\LLM\LlamaIndex_LLM").load_data()
    index = VectorStoreIndex.from_documents(doc)
    index.storage_context.persist()         #Stored in Vector Store
    f=open("Files.txt","w")
    for x in file_dir:
        f.write(x)
    
else:
    index=load_index_from_storage(storage_context=StorageContext.from_defaults(persist_dir=Vector_Store))


service_context=ServiceContext.from_defaults(
    llm=llm,
    embed_model=emd,
    text_splitter=text_spilitter,
    prompt_helper=prompt_help
)

query_engine =index.as_query_engine(service_context=service_context)
val=True


print("\tGPT3.5 Reterival using LLAMBA(RAG)\t")
while(val):
    print("1.Wanna Add File to LLM's")
    print("2.Ask Question to LLM's")
    print("3.Quit")
    opt=int(input("Select the option Bruh:\t"))
    print(opt)
    if(opt==2):
        while(val):
            print("\n")

            query=str(input("Ask Anything Bruh.....(enter 'quit' to exit & 'Add' add file)\n"))
            print(query)
            if(query=="quit"):
                val=False
                break
            elif((query=="Add")or(query=="add")):
                print("inga")
                select_file()
                doc = SimpleDirectoryReader(r"F:\Projects\LLM\LlamaIndex_LLM").load_data()
                index = VectorStoreIndex.from_documents(doc)
                index.storage_context.persist()         #Stored in Vector Store
                f=open("Files.txt","w")
                for x in file_dir:
                    f.write(x)
                break
            else:
                response = query_engine.query(query)
                print(response)
    elif(opt==1):
        select_file()
        doc = SimpleDirectoryReader(r"F:\Projects\LLM\LlamaIndex_LLM").load_data()
        index = VectorStoreIndex.from_documents(doc)
        index.storage_context.persist()         #Stored in Vector Store
        f=open("Files.txt","w")
        for x in file_dir:
            f.write(x)
    elif(opt==3):
        break
    else:
        print("Not an option!!!")
        