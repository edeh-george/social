from fastapi import FastAPI, Query, Path, Body, Request
from pydantic import BaseModel

class Product(BaseModel):
    prodId:int
    prodName:str
    price:float
    stock:int


app = FastAPI()


@app.post("/product")
async def addnew(request: Request, product:Product):
    return product

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="main:app", port=8443, log_level="info")

