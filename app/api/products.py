from pathlib import Path
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.products import CreateProduct
from app.models.product import Product,ProductImage,Category
from app.crud.product import find_product,find_category,get_products,find_products_with_same_name,get_product_image
from app.schemas.products import ProductUpdate,ProductResponse
from datetime import datetime,timezone
import shutil
import uuid

router = APIRouter(prefix="/product",tags=["Products"])


UPLOAD_PATH = Path("uploads")
UPLOAD_PATH.mkdir(exist_ok=True)


@router.post("/add",response_model=ProductResponse)
def add_product(product_data:CreateProduct,session:Session=Depends(get_session)):

    product_exists = find_product(session,product_data.name)

    if product_exists:
       raise HTTPException(status_code=400, detail=f"Product '{product_data.name}' already exists")

    new_product = Product(name=product_data.name,
                          stocks=product_data.stocks,
                          price=product_data.price,
                          description=product_data.description,
                         )
    
    session.add(new_product)

    session.flush()


    for category in product_data.categories:

        category_exists = find_category(session,category)

        if category_exists:
           new_product.categories.append(category_exists)
        else:
            new_category = Category(name=category)
            session.add(new_category)
            new_product.categories.append(new_category)

    
    session.commit()
    session.refresh(new_product)
    

    return ProductResponse(
        id=new_product.id,
        name=new_product.name,
        price=new_product.price,
        stocks=new_product.stocks,
        description=new_product.description,
        created_at=new_product.created_at,
        updated_at=new_product.updated_at,
        categories=[cat.name for cat in new_product.categories] 
    )

@router.get("/list")
def get_products_list(session:Session=Depends(get_session)):
     products = get_products(session)


     result = []
     for product in products:
        product_image = get_product_image(session,product.id)

        result.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stocks": product.stocks,
            "description": product.description,
            "images": [img for img in product_image],
            "categories": [cat.name for cat in product.categories],
            "image_count": len(product.images),
            "category_count": len(product.categories)
        })
    
     return {
        "count": len(result),
        "data": result
    }
     

@router.patch("/update",response_model=ProductResponse)
def update_product(new_product:ProductUpdate,session:Session=Depends(get_session)):
    product = session.get(Product,new_product.id)
    
    if product is None:
        raise HTTPException(status_code=400,detail="Product not found")

    if new_product.name and new_product.name == product.name and find_products_with_same_name(session,new_product.id,new_product.name):
            raise HTTPException(status_code=400,detail=f"Product with name of {new_product.name} has existed already!")


    updated_fields = new_product.model_dump(exclude_unset=True,exclude={"id","images","categories"})


    for field,value in updated_fields.items():
        setattr(product,field,value)


    if new_product.images is not None:
        existing_urls = {image.image_url for image in product.images}
        print("====",existing_urls)
        for idx,url in enumerate(new_product.images):

            if url in existing_urls:
                continue

            product.images.append(ProductImage(product_id=product.id,name=f"{product.name}_image_{idx}",image_url = url,alt_text=f"{product.name}_image_{idx}"))
            

    if new_product.categories is not None:
        existed_categories = {cat.name for cat in product.categories}

        for category_name in new_product.categories:
            if category_name in existed_categories:
                continue

            category =find_category(session,category_name)

            if category is None:
                category = Category(name=category_name)
                session.add(category)
                session.flush()
                product.categories.append(category)
            
            
    product.updated_at = datetime.now(timezone.utc)

    session.commit()
    session.refresh(product)

    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        stocks=product.stocks,
        description=product.description,
        created_at=product.created_at,
        updated_at=product.updated_at,
        images=[img.image_url for img in product.images],  
        categories=[cat.name for cat in product.categories] 
    )




@router.post("/upload/{product_id}/image")
def upload_image(product_id:int,file:UploadFile =File(...),session:Session=Depends(get_session)):

    product = session.get(Product,product_id)


    if not product:
        raise HTTPException(status_code=404,detail="Product not found")



    filename = file.filename
    filepath = UPLOAD_PATH / filename



    try:
        with open(filepath,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
    except:
        raise HTTPException(status_code=400,detail="File path does not exist")

    image  = ProductImage(product_id=product_id,
                                       name=f"{file.filename}",
                                       image_url=f"uploads/{file.filename}",
                                       alt_text=f"{filename}")
    

    session.add(image)
    session.commit()
    session.refresh(image)

    return image


    
    

    
             
             
    




    

     
    
