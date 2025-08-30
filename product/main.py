from sqlmodel import select, SQLModel
from fastapi import FastAPI,HTTPException,status
from fastapi.concurrency import asynccontextmanager
from .database import SessionDep, create_db_and_tables
from .models import Product,ProductReplace,ResponseModel

# Model for PUT request - complete replacement (all fields required)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")    
app = FastAPI(lifespan=lifespan)

@app.post('/product',status_code=status.HTTP_201_CREATED)
def add_product(product:Product,session:SessionDep):
    session.add(product)
    session.commit()
    session.refresh(product)
    return {"status": "success", "message": "Product added successfully", "data": product}

@app.get('/product')
def get_allProduct(session:SessionDep)->list[Product]:
   product = session.exec(select(Product)).all()
   return product

@app.get('/product/{productid}',response_model=ResponseModel)
def get_product_byId(session:SessionDep,productid:int)->Product:
    product = session.get(Product,productid)
    if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return product

@app.delete('/product/{productId}')
def delete_product(productId:int,session:SessionDep):
    product = session.get(Product,productId)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    session.delete(product)
    session.commit()
    return{f"product deleted with id {productId}"}

@app.put('/product/{productid}')
def replace_product(productid: int, product_data: ProductReplace, session: SessionDep):
    product = session.get(Product, productid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    
    session.commit()
    session.refresh(product)
    return {"status": "success", "message": "Product replaced successfully", "data": product}

@app.patch('/product/{productid}')
def update_product(productid:int,session:SessionDep,product_update:Product):
    product = session.get(Product,productid)
    if not product:
       raise HTTPException(status_code=404, detail="product not found")
    update_product = product_update.model_dump(exclude_unset=True)
    for filed,value in update_product.items():
        setattr(product,filed,value)
    session.commit()
    session.refresh(product)
    return  {"status": "success", "message": "Product updated successfully", "data": product}