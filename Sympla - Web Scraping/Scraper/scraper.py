import os
import time
import re
import json
import bs4 as bs
import urllib.request
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class selenium:
    def __init__(self):
        self.error = None

    def scraperURL(self, tipoEvento):
        try:
            self.driver = webdriver.Firefox()

            site  = 'https://www.sympla.com.br/eventos/' + tipoEvento
            self.driver.get(site)
            self.driver.implicitly_wait(20)

        except:
            self.driver.close()
            self.error = 'Error'
    
    def numeroDeEventos(self):
        try:
            nEventos = self.driver.find_element_by_xpath('//*[@id="all-results-list"]/div[1]/div/h3/strong').text
            return nEventos
        except:
            #self.driver.close()
            self.error = 'Error'

    def carregarMaisEventos(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="more-events"]').click()
        except:
            #self.driver.close()
            self.error = 'Error'
    
    def recuperaURLEventos(self, pagina, posicao):
        try:
            if pagina == 1:
                url = self.driver.find_element_by_xpath('//*[@id="events-grid"]/div/div/ul/li[' + str(posicao) + ']/a').get_attribute("href")
            
            if pagina > 1:
                pagina = pagina - 1            
                url = self.driver.find_element_by_xpath('//*[@id="events-grid"]/ul[' + str(pagina) + ']/li[' + str(posicao) + ']/a').get_attribute("href")
            return url
        except:
            #self.driver.close()
            self.error = 'Error'
            url = 'Error'
            return url

    def fecharConexao(self):
        self.driver.close()

    def recuperaDadosEventos(self, url):
        try:

            dadosEventos = []
            listaValorIngresso = []

            source = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(source,'lxml')

            # Scrap Tabela Valores
            table = soup.find('table')
            table_rows = table.find_all('tr')

            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                listaValorIngresso.append(row)
                #print(row)
            
            listaValorIngresso.pop(0)

            dadosEventos.append(listaValorIngresso)

            # Scrap Nome Evento
            nome_evento = soup.find_all('h1', class_ = 'event-name')
            for x in nome_evento:
                nome_Evento = x.text
                #print(nome_Evento)

            dadosEventos.append(nome_Evento)

            #Scrap Local
            local = soup.find_all('div', class_ = 'event-info-city')
            for x in local:
                local = x.text
                #print(local)

            dadosEventos.append(local)

            #Scrap Data
            data = soup.find_all('div', class_ = 'event-info-calendar')
            for x in data:
                data = x.text
                #print(data)

            dadosEventos.append(data)

            return dadosEventos

        except:
            dadosEventos.clear()
            dadosEventos.append("Error")
            return dadosEventos
