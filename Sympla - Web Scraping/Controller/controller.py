from datetime import datetime, timedelta
import time

from Scraper.scraper import selenium
from Controller.controllerBanco import conBanco
from Controller.controllerAuxiliar import auxiliar

class controller:
    def __init__(self):
        self.error = None

    def recuperaURL(self):
        #instanciando classes necessarias
        scraper = selenium()
        banco = conBanco()

        while True:
            #Recupera o tipo do evento
            event = banco.recuperaTipoEvento()

            if event != None:

                scraper.scraperURL(event[0])

                nElementos = scraper.numeroDeEventos()
                nPaginas = int(round((int(nElementos) / 21),0))

                for i in range(nPaginas):
                    pagina = i + 1
                    for j in range(21):
                        posicao = (j + 1)
                        print('Pagina - ' + str(pagina) + ' # Posição - ' + str(posicao))

                        url = scraper.recuperaURLEventos(pagina, posicao)
                        print(url)

                        if url != 'Error':

                            origem = url.split(".br/")[0]
                            origem = origem + '.br'

                            if origem == 'https://www.sympla.com.br':
                                idEvento = url.split("__")[1]
                                print(idEvento)
                            else:
                                idEvento = url.split("event/")[1]

                            #verifica duplicatas
                            duplicatas = banco.verificaDuplicata(idEvento)
                            if duplicatas == 0:
                                #salva as urls encontradas no banco de dados
                                banco.salvaURL(url, idEvento, event[0], origem)

                                self.recuperaEventos(url, idEvento)

                            else:
                                print('-> Registro Duplicado !')

                    print("#--------------------------------------------------------#")
                    scraper.carregarMaisEventos()
                    time.sleep(1)
                
                scraper.fecharConexao()
                banco.encerraTipoEvento(event[0])

            else:
                banco.zeraTipoEvento()

    def recuperaEventos(self, url, idEvento):
        #instanciando classes necessarias
        scraper = selenium()
        banco = conBanco()
        aux = auxiliar()

        print(url + " --- " + str(idEvento))

        dadosEventos = scraper.recuperaDadosEventos(url)

        if dadosEventos[0] != 'Error':
            nomeEvento = dadosEventos[1]
            local = dadosEventos[2]
            data = dadosEventos[3]
            listaValorIngresso = dadosEventos[0]

            dataArrumada = aux.arrumaDataNovo(data)

            aux.diaDaSemana(idEvento, dataArrumada)

            localizacao = aux.arrumaLocalizacao(local)

            novoIngresso = aux.arrumaValorIngreesso(listaValorIngresso)

            banco.salvaValoresIngressos(idEvento, novoIngresso)

            maiorIngresso = max(novoIngresso, key=float)

            nome_evento = nomeEvento
            nome_evento = nome_evento.replace("'", "")
            local = aux.arrumaLocal(local)
            cidade = localizacao[0]
            cidade = cidade.replace("'", "")
            estado = localizacao[1]
            data_inicio = dataArrumada[0]
            data_fim = dataArrumada[1]
            qnt_lotes = len(novoIngresso)
            valor_ingresso = maiorIngresso

            banco.alteraDadosEventos(nome_evento, local, cidade, estado, data_inicio, data_fim, qnt_lotes, valor_ingresso, idEvento)

        else:
            banco.alteraDadosEventosErro(idEvento)
