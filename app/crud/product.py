from sqlmodel import Session,select
from sqlalchemy.orm import joinedload
from app.models.product import Product,Category,ProductImage
from app.schemas.products import ProductQuery


def create_product(session:Session,product:Product):
   
   session.add(product)

   session.commit()

   session.refresh(product)

   return product



def get_products(session:Session):

    query =  select(Product).options(
            joinedload(Product.images),
            joinedload(Product.categories)
        )
    
    products = session.exec(query).unique().all()

    return products
   
   

def find_product(session:Session,product_name:str):

   query = select(Product).where(Product.name == product_name)
      
   return session.exec(query).first()

   


def find_category(session:Session,category_name:str):
   query = select(Category).where(Category.name == category_name)

   return session.exec(query).first()
   

def find_products_with_same_name(session:Session,new_product_name:str,new_product_id:str):
    return session.exec(select(Product).where(Product.id != new_product_id,new_product_name == Product.name)).first()


def find_image_in_product(session:Session,image_url:str,product_id:str):
   return session.exec(select(ProductImage).where(ProductImage.product_id == product_id,ProductImage.image_url==image_url)).first()
   