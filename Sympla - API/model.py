from banco import bancoPostgre


class modelo:

    def __init__(self):
        self.error = None

    def recuperaUmEvento(self, idevento):
        conexao = bancoPostgre()

        con = conexao.getConexao('postgres')
        cur = con.cursor()                
            
        sql = "select url, nome_evento, local, cidade, estado, data_inicio, data_fim, qnt_lotes, valor_ingresso, data_create, tipo_evento from tb_eventos where idevento = " +str(idevento)

        cur.execute(sql)
        row = cur.fetchone()

        con.commit()
        con.close()
        return(row)