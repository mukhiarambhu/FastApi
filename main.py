from fastapi import FastAPI

#creating instance of application 
app = FastAPI()

#decorator that handle request at / path
@app.get("/")
def Index():
    return "Hello World"

@app.get("/home")
def index():
    return "Home"


# path parameter , a parameter passed to path with type

@app.get('/property/{id}')
def getProperty(id:int):  # this type ensure id passed is int always not other data type
    return f'the property is {id}'    


#queryparameter - it is passed to the function not to path 
# and is accessed with serveradress/path?id=10 --> id=10 after ? is query parameter

@app.get("/products")
def products(id:int=0, price:int=100): # default value to query parameter
    return {f'product is {id} and price is {price}'}

# we can have path parameter and queryparametr as well

@app.get('/user/{id}')
def getuser(id:int,parentId:int):
    return {f"user id for user is {id} and parentId is {parentId}"}