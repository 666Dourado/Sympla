from datetime import datetime, timedelta
import time

from Controller.controllerBanco import conBanco

class auxiliar:

    def __init__(self):
        self.error = None

    def convertMes(self, mes):
        if mes == 'janeiro':
            return '01'
        elif mes == 'fevereiro':
            return '02'
        elif mes == 'março':
            return '03'
        elif mes == 'abril':
            return '04'
        elif mes == 'maio':
            return '05'
        elif mes == 'junho':
            return '06'
        elif mes == 'julho':
            return '07'
        elif mes == 'agosto':
            return '08'
        elif mes == 'setembro':
            return '09'
        elif mes == 'outubro':
            return '10'
        elif mes == 'novembro':
            return '11'
        elif mes == 'dezembro':
            return '12'

    def arrumaLocalizacao(self, local):
        localizacao = []
        
        for i in range(len(local)):
            i = len(local) - i
            letra = local[i:]
            pletra = letra[:1]
            if pletra == "-":
                localidade = local[i:]

                cidade = localidade.split(",")[0]
                cidade = cidade.replace('- ', '')

                estado = localidade.split(",")[1]
                estado = estado.replace(' ', '')

                localizacao.append(cidade)
                localizacao.append(estado)

                return localizacao
        
        localizacao.append('Evento Online')
        localizacao.append('Evento Online')

        return localizacao

    def arrumaDataNovo(self, data):
        try:
            datas = []

            data1 = data.split("-")[0]
            data1_corrigido = self.arrumaTextoDataInicio(data1)

            dia = data1_corrigido.split(" ")[0]
            mes = data1_corrigido.split(" ")[2]
            ano = data1_corrigido.split(" ")[4]
            ano = ano.replace(',', '')
            mes_numerico = self.convertMes(mes)
            data_inicio = ano + "-" + mes_numerico + "-" + dia 


            data2 = data.split("-")[1]
            data2_corrigido = self.arrumaTextoDataFim(data2)

            if len(data2_corrigido) > 5:
                dia = data2.split(" ")[1]
                mes = data2.split(" ")[3]
                ano = data2.split(" ")[5]
                ano = ano.replace(',', '')
                mes_numerico = self.convertMes(mes)
                data_fim =  ano + "-" + mes_numerico + "-" + dia 

            else:
                data_fim = data_inicio

            datas.append(data_inicio)
            datas.append(data_fim)

            return datas

        except:
            data_fim = data_inicio
            datas.append(data_inicio)
            datas.append(data_fim)

            return datas

    def arrumaTextoDataInicio(self, data):
        for i in range(len(data)):
            i = len(data) - i
            letra = data[i:]
            pletra = letra[:1]
            if pletra == "0" or pletra == "1" or pletra == "2" or pletra == "3" or pletra == "4" or pletra == "5" or pletra == "6" or pletra == "7" or pletra == "8" or pletra == "9":
                data_corrigido = data[i:]

        return data_corrigido

    def arrumaTextoDataFim(self, data):
        for i in range(len(data)):
            #i = len(data) - i
            letra = data[:i]
            if letra != '':
                pletra = letra[-1]
                if pletra != ' ':
                    data_corrigido = data[:i]

        return data_corrigido
        
    def arrumaValorIngreesso(self, listaValorIngresso):
        novoValor = []
        for row in listaValorIngresso:
            if len(row) == 2:
                row.pop(1)
                if row[0] == '\n\n\n\n\n\n':
                    row.pop(0)
            else:
                row.pop(0)

            for x in row:
                valor = self.obtemValorIngresso(x)
                novoValor.append(valor)

        return novoValor
    
    def obtemValorIngresso (self, valor):
        try:
            nvalor = valor.split("$ ")[1]
            for i in range(len(nvalor)):
                valor = nvalor[:i]
                if valor != '':
                    pletra = valor[-1]
                    if pletra == ' ' or pletra == '\n' :
                        valor = valor.replace(' ', '')
                        valor = valor.replace('\n', '')
                        valor = valor.replace('\xa0', '')
                        valor = valor.replace('.', '')
                        valor = valor.replace(',', '.')

                        teste = float(valor) + float(valor)
                        return valor
                
            valor = valor.replace(',', '.')
            teste = float(valor) + float(valor)
            return valor
        except:
            nvalor = 0
            return nvalor

    def arrumaLocal(self, local):
        local = local.replace("\n", "")
        local = local.replace("                                            ", "")
        local = local.replace("                                        ", "")
        local = local.replace("'", "")
        return local

    def diaDaSemana(self, idvento, datas):
        banco = conBanco()

        DIAS = [
            'Segunda',
            'Terça',
            'Quarta',
            'Quinta',
            'Sexta',
            'Sábado',
            'Domingo'
        ]

        data_inicio = datas[0]
        data_fim = datas[1]

        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        quantidade_dias = abs(data_inicio - data_fim)
        quantidade_dias = quantidade_dias.days
        quantidade_dias = quantidade_dias + 1

        for i in range(quantidade_dias):
            nova_data = data_inicio + timedelta(days=i)
            indice_da_semana = nova_data.weekday()
            dia_da_semana = DIAS[indice_da_semana]

            banco.insereDatas(idvento, nova_data, dia_da_semana)