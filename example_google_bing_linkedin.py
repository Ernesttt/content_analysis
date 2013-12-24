from content_analysis.nlp.metrics_reduced import *
from content_analysis.nlp.relevant_topics import *
from content_analysis.wrappers.google import *
import time

nombre_archivo = "carta_prueba.txt"

# Instantiating classes
topicos = Topicos_Relevantes()  
buscador = Google(license=None) # Your license here
metricas = Metricas()

# Customize query
tipo = [u"curso", u"publicacion",u"programa de apoyo", u"empleo", u"evento"]
tipo_archivo = [u"",u"pdf",u"doc",u"ppt"]

# Reading file
texto = topicos.leer_texto(nombre_archivo)

# Obtaining most common words in text
lista_palabras = metricas.elementos_mas_frecuentes_texto(texto,3)

# Obtaining best bigrams in text
lista_bigramas  = topicos.construcciones_sintacticas_bigramas(texto)

# Obtaining best trigrams in text
lista_trigramas = topicos.construcciones_sintacticas_trigramas(texto)

list = []

# Searching process...
for x in lista_palabras:
    query = tipo[1] + " " +  x.split(":")[0] + " " + tipo_archivo[1]
    resultado = buscador.search(query)
    time.sleep(1) #needed for google custom search engine
    buscador.write_txt(resultado)
    lista = buscador.result_list(resultado)
    list.append(lista)
'''
for x in lista_bigramas:
    resultado = buscador.search(x)
    time.sleep(1) #needed for google custom search engine
    buscador.write_txt(resultado)
    lista = buscador.result_list(resultado)
    list.append(lista)
    
for x in lista_trigramas:
    resultado = buscador.search(x)
    time.sleep(1) #needed for google custom search engine
    buscador.write_txt(resultado)
    lista = buscador.result_list(resultado)
    list.append(lista)
'''
print list
    
