import requests
from models.models import Producto
from bs4 import BeautifulSoup
from db.database import database
from bson import ObjectId

def scraping():
    url = "https://laika.com.co/category/bog/dog/alimento/todos/todos/todo-para-mascota/1?wpsrc=Google%20AdWords&wpcid=21111222369&wpsnetn=x&wpkwn=&wpkmatch=&wpcrid=&wpscid=&wpkwid=&&device=c&keyword=&placement=&adgroup=&campaign=21111222369&wpsrc=Google%20AdWords&wpcid=21111222369&wpsnetn=x&wpkwn=&wpkmatch=&wpcrid=&wpscid=&wpkwid=&utm_campaign=21111222369&gad_source=1&gad_campaignid=21117975116&gclid=Cj0KCQjwotDBBhCQARIsAG5pinOG-d8IQe_EZLvdfogV900HdZwScF3I-nrc0aSfgWDLDQ8OEzLxI9MaAptBEALw_wcB"
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ''AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/58.0.3029.110 Safari/537.3')}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    productos = []

    for producto in soup.find_all("div", class_="mb-5 min_w_265 mx-auto"):
        nombre = producto.find("h2", class_="text_product_card mb-0").text.strip()   
        precio = producto.find("span", class_="mr-2").text.strip()
        imagen = producto.find("img", class_="img_card_products ml-auto mr-auto mt-3 mb-3 lazy")['src']
        
        perros = Producto(nombre=nombre, precio=precio, imagen=imagen)
        productos.append(perros)
    
    if productos:
        collection = database.get_collection("productos")
        result = collection.insert_many([producto.dict() for producto in productos])
        return len(result.inserted_ids)
    else:
        return None

def delete(id: str):
    collection = database.get_collection("productos")
    try:
        collection.delete_one({"_id": ObjectId(id)})
    except Exception as e:
        print(e)
        return {"message": "Error al eliminar el producto"}
    return {"message": "Productos eliminados"}