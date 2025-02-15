from fastapi import FastAPI

app = FastAPI()

"""
@app.get("/doc")
def newOne():
    return {"message": "Hello, World!"}
"""


@app.post("/document/upload")
def upload_file():
    pass
