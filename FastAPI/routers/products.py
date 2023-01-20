from fastapi import APIRouter


router = APIRouter(
    prefix="/products",
    tags=["products"], # para agrupar en la doc
    responses={404: {"message": "No encontrado"}})


products_list = ["Producto 1","Producto 2","Producto 3","Producto 4","Producto 5"]


# Get
@router.get("/")
async def products():
    return products_list

# Get
@router.get("/{id}")
async def products(id: int):
    return products_list[id]

