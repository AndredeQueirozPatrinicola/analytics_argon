from django.db import connections

from datetime import datetime

class Etl:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()
        self.anos = [i for i in range(int(datetime.now().year) - 6, int(datetime.now().year) + 1)]

    def pega_dados_por_ano(self, coluna, order_by=False):
        select = f"SELECT ag.{coluna}"
        query = f"""
                    FROM graduacoes g
                    JOIN alunos_graduacao ag ON g.numeroUSP = ag.numeroUSP
                    GROUP BY ag.{coluna}
                 """ 
        somas = []
        for ano in self.anos:
            somas.append(f", SUM(CASE WHEN ({ano} >= YEAR(dataInicioVinculo)) AND ({ano} <= YEAR(dataFimVinculo) OR dataFimVinculo IS NULL) THEN 1 END) AS '{ano}'")

        somas = "".join(somas)

        if order_by:
            query = query + f"""
                            ORDER BY {order_by}
                            """

        query = f"""
                    { select }
                    { somas  }
                    { query }
                 """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def conta_pessoa_por_categoria(self, tabela, situacao):
        # try:
            self.cursor.execute(f"""
                                    SELECT COUNT(*) 
                                    FROM {tabela} g 
                                    WHERE situacao = '{situacao}';
                                """)
            return self.cursor.fetchall()
        # except:
        #     raise Exception("Não foi possivel realizar a query") 
