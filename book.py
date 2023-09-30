#Importamos las librerias
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from mongo import MongoConnection
#Creamos la conexión a la base de datos
db_client = MongoConnection().client
db = db_client.get_database('LIBROS')
col = db.get_collection('GENERO-TERROR')
#Inicializar el controlador WebDriver de Chrome
driver = webdriver.Chrome()
#Abrir la página web
driver.get("https://www.librimundi.com/")
time.sleep(3)
#Buscamos la barra search para poder escribir nuestra búsqueda
search_book= driver.find_element(By.XPATH, '//*[@id="buscador"]')
search_book.send_keys('terror')
time.sleep(8)
#Buscamos los titulos de los libros para poder extraer la información
name_books= driver.find_elements(by=By.CLASS_NAME, value= "info-main")
#Iterar a traves de la lista de elementos name_books
for i in range(len(name_books)):
    nombre_libro = name_books[i].text
    document = {
        "info_books": nombre_libro,
    }
# Está insertando un documento en la colección
    col.insert_one(document=document)
    print(nombre_libro)
    print("-" * 30)
# Cierra la página web
driver.close()