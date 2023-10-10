
import asyncio
import io
import json
import base64
import os
from typing import Any, AnyStr, Dict, Generic, List, Optional, TypeVar, Union
import uvicorn
from fastapi import FastAPI, File, Form, Header, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from caesaraicontractqa import CaesarAIContractQA
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
caesarcrud = CaesarCRUD()
caesarcreatetables = CaesarCreateTables()
caesarcreatetables.create(caesarcrud)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

table="contracts"
# https://fastapi.tiangolo.com/advanced/events/
@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Hello World"

@app.post("/caesaraicontractqa") # POST # allow all origins all methods.
async def caesaraicontractqa(question: Optional[str] = Form(None),filename: Optional[str] = Form(None),file: Optional[Union[UploadFile,str]] = File(None),filetype : Optional[str] = Form(None),help: Optional[str] = Form(None)):  
    try:
        if help:
            return {"help":r"{'question':'WHEN AND WITH WHOM DO WE SHARE YOUR PERSONAL INFORMATION?','filename':'test','file':[file,str],'filetype':'pdf/txt'}"}
        if type(file) == str:
            contract_data = file
            caesaraiqa = CaesarAIContractQA(data_text=contract_data)
            caesaraiqa.create_db_document(data_source_type="TXT")
            result  =  caesaraiqa.ask_question(question=question, language="ENGLISH")
            return result
            
        else:
            file_data = await file.read()
            #print(file_data)
            contract_data = io.BytesIO(file_data)
            output_name =  "output.txt" if filetype.upper() == "TXT" else "output.pdf"
            with open(output_name, "wb") as f:
                f.write(contract_data.getbuffer())
            caesaraiqa = CaesarAIContractQA(data_source_path=output_name)
            caesaraiqa.create_db_document(data_source_type=filetype.upper())
            result  =  caesaraiqa.ask_question(question=question, language="ENGLISH")
            os.remove(output_name)
            return result
            
            


    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}
    
@app.post("/postcontract") # POST # allow all origins all methods.
async def postcontract(filename: str = Form(),file: Union[UploadFile,str] = Form(...),contractfile: Optional[Union[UploadFile,str]] = File(None)):  
    try:
        contractfields = caesarcreatetables.contractfields
        condition = f"filename = '{filename}'"
        if type(file) != str:
            filecsv = await file.read()
        else:
            filecsv = file
        if type(contractfile) != str:
            contractfileimg = await contractfile.read()
        else:
            contractfileimg = contractfile
        file_exists = caesarcrud.check_exists(("filename",),table,condition)
        if not file_exists:
            result = caesarcrud.post_data(contractfields,(filename,filecsv,contractfileimg),table)
            if result:
                return {"message":"contract data was posted."}
            else:
                return {"error":"post error."}
        else:
            res_update = caesarcrud.update_data(("filename",),(filename,),table,condition)
            if res_update:
                if type(contractfile) != str:
                    caesarcrud.update_blob("contractfile",contractfileimg,table,condition)
                else:
                    caesarcrud.update_data(("contractfile",),(contractfileimg,),table,condition)
                return {"message":"contract data was replaced."}
            else:
                return {"error":"replace error."}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}
@app.get("/getcontract") # POST # allow all origins all methods.
async def getcontract(filename:str):  
    try:
        contractfields = caesarcreatetables.contractfields
        condition = f"filename = '{filename}'"
        file_exists = caesarcrud.check_exists(("filename",),table,condition)
        if file_exists:
            result = caesarcrud.get_data(contractfields,table,condition)[0]
            filecsv = result["file"]
            contractfileimg = result["contractfile"]  #base64.b64encode(bytes.fromhex(result["contractfile"].hex())).decode()
            return {"filename":result["filename"],"file":filecsv,"contractfileimg":contractfileimg}
        else:
            return {"error":"file doesn't exist."}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}
    
@app.get("/getallcontractnames") # POST # allow all origins all methods.
async def getallcontractnames():  
    try:
        files_exists = caesarcrud.check_exists(("*",),table)
        if files_exists:
            result = caesarcrud.get_data(("filename",),table)
            return {"filenames":result}
        else:
            return {"error":"file doesn't exist."}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}



@app.delete("/deletecontract") # POST # allow all origins all methods.
async def deletecontract(filename:str):  
    try:
        condition = f"filename = '{filename}'"
        file_exists = caesarcrud.check_exists(("filename",),table,condition)
        if file_exists:
            result = caesarcrud.delete_data(table,condition)
            if result:
                return {"message":"file was deleted."}
            else:
                return {"error":"delete error"}
        else:
            return {"error":"file doesn't exist."}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}

async def main():
    config = uvicorn.Config("main:app", port=7860, log_level="info",host="0.0.0.0",reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())