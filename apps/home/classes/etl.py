from django.db import connections

from datetime import datetime

class Etl:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()
        self.anos = [i for i in range(int(datetime.now().year) - 6, int(datetime.now().year) + 1)]

    def pega_dados_por_ano(self, coluna, order_by='', where=''):
        try:
            select = f"SELECT ag.{coluna}"
            _from = f'FROM graduacoes g'
            join = f'JOIN alunos_graduacao ag ON g.numeroUSP = ag.numeroUSP'
            group_by = f'GROUP BY ag.{coluna}'

            if where:
                where = f"WHERE g.nomeCurso = '{where}'"

            if order_by:
                order_by = f"ORDER BY {order_by}"

            sum = []
            for ano in self.anos:
                sum.append(f", SUM(CASE WHEN ({ano} >= YEAR(dataInicioVinculo)) AND ({ano} <= YEAR(dataFimVinculo) OR dataFimVinculo IS NULL) THEN 1 END) AS '{ano}'")
            sum = "".join(sum)
            
            query = f"""
                        {  select  }
                        {   sum    }
                        {  _from   }
                        {  join    }
                        {  where   }
                        { group_by }
                        { order_by }
                    """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except:
            raise Exception("Não foi possivel realizar a query") 
        
    def conta_pessoa_por_categoria(self, tabela, situacao):
        try:
            self.cursor.execute(f"""
                                    SELECT COUNT(*) 
                                    FROM {tabela} g 
                                    WHERE situacaoCurso = '{situacao}';
                                """)
            return self.cursor.fetchall()
        except:
            raise Exception("Não foi possivel realizar a query") 
