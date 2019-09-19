from datetime import datetime
from Model.banco import bancoPostgre

class conBanco:

    def __init__(self):
        self.error = None

    def salvaURL(self, url, idEvento, tipo_evento, origem):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        query_1 = "insert into tb_eventos (url, idevento, nome_evento, local, cidade, estado, data_inicio, data_fim, descricao, produtor, qnt_lotes, valor_ingresso, data_create, atualizado, tipo_evento, origem)" 
        query_2 = "VALUES( '" + url + "'," + str(idEvento) + "," + "'-'" + "," + "'-'" + "," + "'-'" + "," +"'-'" + ",'" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "','" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "'," + "'-'" + "," +  "'-'"  + "," + str(0) + "," +str(0) + ",'" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "'," + str(0) + ",'" + tipo_evento + "','" + origem + "')"
        sql = query_1 + query_2

        cur.execute(sql)
        con.commit()
        con.close()

    def verificaDuplicata(self, idEvento):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "select count(*) from tb_eventos where idevento = " +str(idEvento)

        cur.execute(sql)
        row = cur.fetchone()

        qnt = row[0]
        con.commit()
        con.close()
        return(qnt)


    def salvaValoresIngressos(self, idEvento, listaIngresso):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()

        count = 1
        for row in listaIngresso:

            query_1 = "insert into tb_valoringresso (idevento, lote, valor_ingresso)" 
            query_2 = "VALUES(" + str(idEvento) + "," + str(count) + "," + str(row) + ")"
            sql = query_1 + query_2

            cur.execute(sql)
            con.commit()
            count = count + 1


        con.close()

    
    def alteraDadosEventos(self, nome_evento, local, cidade, estado, data_inicio, data_fim, qnt_lotes, valor_ingresso, idevento):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "update tb_eventos set nome_evento = '" + str(nome_evento) + "'," + " local = '" + str(local) + "'," + " cidade = '" + str(cidade) + "'," + " estado = '" + str(estado) + "'," + " data_inicio = '" + str(data_inicio) + "'," + " data_fim = '" + str(data_fim) + "'," + " qnt_lotes = " + str(qnt_lotes) + "," + " valor_ingresso = " + str(valor_ingresso) + ", atualizado = 1  where idevento = " + str(idevento)
        
        cur.execute(sql)
        con.commit()
        con.close()


    def alteraDadosEventosErro(self, idevento):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "update tb_eventos set atualizado = 2  where idevento = " + str(idevento)
        
        cur.execute(sql)
        con.commit()
        con.close()


    def insereDatas(self, idEvento, data_evento, dia_semana):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()

        query_1 = "insert into tb_datas (idevento, data_evento, dia_semana)" 
        query_2 = "VALUES(" + str(idEvento) + ",'" + str(data_evento) + "','" + str(dia_semana) + "')"
        sql = query_1 + query_2

        cur.execute(sql)
        con.commit()
        con.close()

    def recuperaTipoEvento(self):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "select tipo_evento from tb_tipoevento where status = 0 limit 1"

        cur.execute(sql)
        row = cur.fetchone()

        con.commit()
        con.close()
        return(row)


    def encerraTipoEvento(self, tipo_evento):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "update tb_tipoevento set status = 1  where tipo_evento = '" + tipo_evento + "'"
        
        cur.execute(sql)

        con.commit()
        con.close()
    
    def zeraTipoEvento(self):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "update tb_tipoevento set status = 0 "
        
        cur.execute(sql)
        con.commit()
        con.close()