from fastapi import FastAPI
from pydantic import BaseModel,HttpUrl
from typing import Set

class User(BaseModel):
    name:str
    email:str
    age:int
    

class Image(BaseModel):
    url:HttpUrl
    name:str

class Product(BaseModel):
    id:int
    name:str
    price:int
    discount:int
    discounted_price: float
    tags : Set[str]= []
    images:Image
#creating instance of application 
app = FastAPI()

@app.post('/user')
def user(user:User):
    return user

@app.post('/addproduct/{productId}')
def addProduct(produt:Product,productId:int):
    produt.id = productId
    produt.discounted_price = produt.price - (produt.price*produt.discount)/100
    return produt

@app.post('/purchase')
def purchase(user:User,product:Product):
    return{"user":user,"product":product}