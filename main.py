import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from mongo import MongoConnection

db_client = MongoConnection().client
db = db_client.get_database('JUEGOS')
col = db.get_collection('PS4')

#Inicializar el controlador WebDriver de Chrome
driver = webdriver.Chrome()
#Abrir la página web
driver.get("https://store.playstation.com/es-ec/view/25d9b52a-7dcf-11ea-acb6-06293b18fe04/e62084eb-203f-11eb-aadc-062143ad1e8d")
offers= driver.find_element(By.LINK_TEXT, 'Ofertas')
offers.click()
time.sleep(5)
offers1= driver.find_element(By.XPATH, '//*[@id="932dc7b8-fe6a-11ea-aadc-062143ad1e8d-0d1c186d-4b9d-11ee-840b-3e19c375a217"]' )
offers1.click()
time.sleep(9)
#Encontrando los elementos de la página web
plays = driver.find_elements(by=By.CSS_SELECTOR, value="#main")
# Creamos la función para extraer loa datos
def extraer_datos_pagina_actual():
#utilizamos el método para extracción de datos
    for f in plays:
        name = f.find_element(by=By.CSS_SELECTOR, value= "div.psw-l-w-1\/1:nth-child(2)").text

        lineas = name.split('\n')
        name1 = lineas[0]
        for linea in lineas:
            if "US$" in linea:
                precio = linea
                break
        else:
            precio = "Precio no encontrado"
        document = {
         "name": name,
         "precio":precio,
     }
        col.insert_one(document=document)
        print('=' * 40)
        print(name)
        print(precio)
        print('=' * 40)
# Iterar a través de las páginas
pag_actual = 1
pag_totales = 1
while pag_actual <= pag_totales:
    print(f"Extrayendo datos de la página {pag_actual}...")
    extraer_datos_pagina_actual()
#Creamos la función para dar click y pasar a la siguiente página
    next_button = driver.find_element(by=By.CSS_SELECTOR, value= "button.psw-button:nth-child(3)")
    next_button.click()
    time.sleep(2)
    pag_actual += 1
driver.close()
