import scrapy
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import random
from scrapy.selector import Selector
import sys
import csv

localidades = [['Álava','Albacete','Alicante','Almería','Andalucía','Aragon','Asturias','Ávila'],
               ['Badajoz','Barcelona','Burgos'],
               ['Cáceres','Cádiz','Cantabria','Castellón','Castilla y León','Castilla-La Mancha','Cataluña','Ciudad Real','Comunidad Valenciana','Comunidad Foral de Navarra','Córdoba','Cuenca'],
               ['Extremadura'],
               ['Galicia','Gerona','Girona','Granada','Guadalajara','Guipúzcoa'],
               ['Huelva','Huesca'],
               ['Islas Baleares'],
               ['Jaén'],
               ['La Coruña','La Rioja','Las Palmas','León','Lérida','Lleida','Lugo'],
               ['Madrid','Malaga','Murcia'],
               ['Navarra'],
               ['Orense'],
               ['Palencia','Pontevedra'],
               ['Salamanca','Santa Cruz de Tenerife','Segovia','Sevilla','Soria'],
               ['Tarragona','Teruel','Toledo'],
               ['Valencia','Valladolid','Vizcaya'],
               ['Zamora','Zaragoza']]


#anadir = []

class Datos(Item):
    Id = Field()
    Descripcion = Field()
    Url = Field()
    Localizaciones = Field()
    Nombres = Field()
    Fechas = Field()

class BOESpider(CrawlSpider):
    name = "Boe"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    } 

    allowed_domains = ["boe.es"]
    start_urls = ["https://www.boe.es/diario_boe/ultimo.php"]
    #start_urls = ["https://www.boe.es/diario_boe/txt.php?id=BOE-B-2022-7320"]
    #start_urls = ["https://www.boe.es/diario_boe/txt.php?id=BOE-A-2022-3292"]

    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/diario_boe/txt.php',
            ), follow=True, callback='parse'),
    )

    

    def parse(self, response):
        encontrado = False
        sel = Selector(response)
        item = ItemLoader(Datos(), sel)
        locali = []
        item.add_xpath('Id', '//div[@class="metadatos"]/dl/dd[4]/text()') #Sacar Id
        url = response.url #Se obtiene la url actual.
        item.add_value("Url", url)
        item.add_xpath('Descripcion', '//h3[@class="documento-tit"]/text()') #Sacar Descripcion
        firmas = response.xpath('//p[starts-with(@class, "firma_")]')#Firma
        if(firmas == []):
            item.add_value("Nombres", None) #Añadir Nombres
        else:
            for i, elem in enumerate(firmas):
                texto = elem.xpath('./text()').get()
                textonopartido = texto
                texto = texto.split()
                encontrado = False
                with open('nombres-2015.csv', encoding='utf8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        separadito = row[0].split()
                        if(separadito[0].lower() == texto[0].lower() and encontrado == False):
                            encontrado = True
                            item.add_value("Nombres", textonopartido) #Añadir Nombres


        try:
            titles = response.xpath('//div[@id="textoxslt"]/dl/dt')#Titulo
        except:
            print('No se encontro Titulo.')
        else:
            for i, elem in enumerate(titles):
                texto = elem.xpath('./text()').get()
                separadito = texto.split()
                for palabra in enumerate(separadito):
                    numero = posicion(palabra)
                    palabra = limpiar(palabra)
                    locali = buscar(numero, palabra, locali)

        try:
            subtitles = response.xpath('//div[@id="textoxslt"]/dl/dd/dl/dt')#Sub-Titulo
        except:
            print('No se encontro Sub-Titulo')
        else:
            for i, elem in enumerate(subtitles):
                texto = elem.xpath('./text()').get()
                separadito = texto.split()
                for palabra in enumerate(separadito):
                    numero = posicion(palabra)
                    palabra = limpiar(palabra)
                    locali = buscar(numero, palabra, locali)

        try:
            coment = response.xpath('//div[@id="textoxslt"]/dl/dd/dl/dd')#Comentarios
        except:
            print('No se encontraron Comentarios')
        else:
            for i, elem in enumerate(coment):
                texto = elem.xpath('./text()').get()
                separadito = texto.split()
                for palabra in enumerate(separadito):
                    numero = posicion(palabra)
                    palabra = limpiar(palabra)
                    locali = buscar(numero, palabra, locali)

        try:
            parrafos = response.xpath('//div[@id="textoxslt"]/p')#Parrafos
        except:
            print('No se encontraron Parrafos')
        else:
            for i, elem in enumerate(parrafos):
                texto = elem.xpath('./text()').get()
                separadito = texto.split()
                for palabra in enumerate(separadito):
                    numero = posicion(palabra)
                    palabra = limpiar(palabra)
                    locali = buscar(numero, palabra, locali)
    

        item.add_value("Localizaciones", locali) #Añadir Nombres
        yield item.load_item()



def posicion(palabra):
    if(palabra[1][0]=='a'or palabra[1][0]=='A'):
        pos = 0
    elif(palabra[1][0]=='b'or palabra[1][0]=='B'):
        pos = 1
    elif(palabra[1][0]=='c'or palabra[1][0]=='C'):
        pos = 2
    elif(palabra[1][0]=='e'or palabra[1][0]=='E'):
        pos = 3
    elif(palabra[1][0]=='g'or palabra[1][0]=='G'):
        pos = 4
    elif(palabra[1][0]=='h'or palabra[1][0]=='H'):
        pos = 5
    elif(palabra[1][0]=='i'or palabra[1][0]=='I'):
        pos = 6
    elif(palabra[1][0]=='j'or palabra[1][0]=='J'):
        pos = 7
    elif(palabra[1][0]=='l'or palabra[1][0]=='L'):
        pos = 8
    elif(palabra[1][0]=='m'or palabra[1][0]=='M'):
        pos = 9
    elif(palabra[1][0]=='n'or palabra[1][0]=='N'):
        pos = 10
    elif(palabra[1][0]=='o'or palabra[1][0]=='O'):
        pos = 11
    elif(palabra[1][0]=='p'or palabra[1][0]=='P'):
        pos = 12
    elif(palabra[1][0]=='s'or palabra[1][0]=='S'):
        pos = 13
    elif(palabra[1][0]=='t'or palabra[1][0]=='T'):
        pos = 14
    elif(palabra[1][0]=='v'or palabra[1][0]=='V'):
        pos = 15
    elif(palabra[1][0]=='z'or palabra[1][0]=='Z'):
        pos = 16
    else: pos = -1
    return pos



def limpiar(palabra):
    characters = ",./¿!?:;"
    palabrita = palabra[1]
    for x in range(len(characters)):
        palabrita = palabrita.replace(characters[x],"")
    return palabrita

def buscar(posicion, palabra, locali):
    if(posicion != -1):
        for i in range(len(localidades[posicion])):
            if(localidades[posicion][i].lower() == palabra.lower()):          
                locali = anadir(locali, palabra)
    return locali


def anadir(locali, palabra):
    existe = False
    if(len(locali)==0):
        #añadir el nombre de la localidad
        locali.append(palabra)
    else:
        #Buscar si existe la localidad:
        for elem in enumerate(locali):
            #No existe, se Guarda.
            if(elem[1].lower() == palabra.lower()):
                existe = True
        if(existe == False):
            locali.append(palabra)

    return locali
