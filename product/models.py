from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    __tablename__ = "product"
    id:int|None = Field(default=None,primary_key=True,sa_column_kwargs={"autoincrement": True})
    name:str =Field(index=True)
    description:str
    price:int