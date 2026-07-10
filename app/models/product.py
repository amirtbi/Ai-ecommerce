from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,List
from datetime import datetime,timezone



class ProductCategoryLink(SQLModel,table=True):
    product_id:int = Field(foreign_key="product.id",primary_key=True)
    category_id:int = Field(foreign_key="category.id",primary_key=True)

class Category(SQLModel,table=True):
    id:Optional[int] =Field(default=None,primary_key=True)
    name:str = Field(unique=True,index=True)
    products:List[Product] = Relationship(back_populates="categories",link_model=ProductCategoryLink)





class Product(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str = Field(unique=True)
    price:float
    stocks:int = Field(default=0)
    updated_at:Optional[datetime] = None
    description:Optional[str] = None
    images:List[ProductImage] = Relationship(back_populates="product")
    categories:List[Category] = Relationship(back_populates="products",link_model=ProductCategoryLink)
    created_at:datetime = Field(default_factory=lambda:datetime.now(timezone.utc))



class ProductImage(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str = Field(index=True)
    image_url:str
    description:Optional[str] = None
    created_at:datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    product_id:int  =Field(foreign_key="product.id")
    product:Product = Relationship(back_populates="images")
    alt_text :Optional[str] = None
