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
import re

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

    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/diario_boe/txt.php',
            ), follow=True, callback='parse'),
    )

    

    def parse(self, response):
        prueba='oki'
        fecha_valida(prueba)
        '''encontrado = False
        sel = Selector(response)
        item = ItemLoader(Datos(), sel)
        locali = []
        fechas = []
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
                    if(fecha_valida(texto)):
                        print('fecha valida---------------------------------------------------------------------------')
                        print(palabra)
                        #item.add_value("Fechas", palabra) #Añadir Nombres

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
                    if(fecha_valida(texto)):
                        print('fecha valida---------------------------------------------------------------------------')
                        print(palabra)
                        #item.add_value("Fechas", palabra) #Añadir Nombres

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
                    if(fecha_valida(texto)):
                        print('fecha valida---------------------------------------------------------------------------')
                        print(palabra)
                        #item.add_value("Fechas", palabra) #Añadir Nombres

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
                    if(fecha_valida(texto)):
                        print('fecha valida---------------------------------------------------------------------------')
                        print(palabra)
                        #item.add_value("Fechas", palabra) #Añadir Nombres

        item.add_value("Localizaciones", locali) #Añadir Nombres
        yield item.load_item()'''



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


def fecha_valida(cadena):
    frase = "En esta cadena se encuentra 39/2015 2001/01/01 una palabra magica el dia 5 de mayo de 1989 nacio un Heroe, alabado sea."

    #antpatron = r'\s\d+\D+\d+\s|\D' # 1 de mayo de 1989
    antpatron = r'\s\d+\D+\d+\s' # 1 de mayo de 1989
    antpatron1 = r'\s\d+\D+\d+\D' # 1 de mayo de 1989
    antpatron2 = r'\s\d+\D+\d+\s' #39/2015 | 39-2015

    patron = '^(([0-3]{0}|([0-3]{1}))[0-9])( de enero de | de febrero de | de marzo de | de abril de | de mayo de | de junio de | de julio de | de agosto de | de septiembre de | de octubre de | de noviembre de | de diciembre de )(19[0-9]{2}|20[0-9]{2})$'#'1 de marzo de 2011' == True
    patron1 = '^(([0-9]{0}|[0-9]{1})[0-9]{1}\D+(19[0-9]{2}|20[0-9]{2}))$'#39/2015 | 39-2015

    #patron2 = '^(19[0-9]{2}|20[0-9]{2})/(0\d|1[0-2])/(0\d|1[0-9]|2[0-9]|3[0-1])$'#'2001/01/01' == True
    #patron3 = '^(19[0-9]{2}|20[0-9]{2})-(0\d|1[0-2])-(0\d|1[0-9]|2[0-9]|3[0-1])$'#'2001-01-01' == True
    #antpatron = r'\d+\D+\d+\D+\d+' #1989/01/01 | 1989-01-01


    contador = len(frase)
    continuar = True
    nuevafrase = frase;
    i=0
    n=3

    while i < n:
        i = i + 1
        if(re.search(antpatron,nuevafrase) is not None):
            inter = re.search(antpatron,nuevafrase)
            inter = inter.span()
            if(bool(re.search(patron,nuevafrase[inter[0]+1:inter[1]-1])) == False):
                print('patronimportante por lo tanto ha de guardarse')
                #aqui vendra instruccion para Guardar Fecha
                nuevafrase = nuevafrase[inter[1]:]
                print('nueva frase1: ' + nuevafrase)
                #comprobar si la ultima posicion es la ultima posicion es igual a contador
                if(inter[1]==contador):
                    print('final')

        if(re.search(antpatron1,nuevafrase) is not None):
            inter = re.search(antpatron1,nuevafrase)
            inter = inter.span()
           # print(nuevafrase[inter[0]+1:inter[1]])
            if(bool(re.search(patron,nuevafrase[inter[0]+1:inter[1]])) == False):
                print('patronimportante2 por lo tanto ha de guardarse')
                #aqui vendra instruccion para Guardar Fecha
                nuevafrase = nuevafrase[inter[1]:]
                print('nueva frase2: ' + nuevafrase)
                #comprobar si la ultima posicion es la ultima posicion es igual a contador
                if(inter[1]==contador):
                    print('final2')

        if(re.search(antpatron2,nuevafrase) is not None):
            inter = re.search(antpatron2,nuevafrase)
            inter = inter.span()
            print(nuevafrase[inter[0]+1:inter[1]-1])
            if(bool(re.search(patron1,nuevafrase[inter[0]+1:inter[1]-1]))):
                print('patronimportante3 por lo tanto ha de guardarse ')
                #aqui vendra instruccion para Guardar Fecha
                nuevafrase = nuevafrase[inter[1]:]
                print('nueva frase3: ' + nuevafrase)
                #comprobar si la ultima posicion es la ultima posicion es igual a contador
                if(inter[1]==contador):
                    print('final2')    
        
    print('sali del bucle')