from django.db import connections

from datetime import datetime

class Etl:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()
        self.anos = [i for i in range(int(datetime.now().year) - 6, int(datetime.now().year) + 1)]

    def pega_dados_por_ano(self, coluna):
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
        query = f"""
                    { select }
                    { somas  }
                    { query }
                 """
        self.cursor.execute(query)
        return self.cursor.fetchall()

