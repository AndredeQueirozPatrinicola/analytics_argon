from django.db import connections

from datetime import datetime

class Etl:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()
        self.anos = [i for i in range(int(datetime.now().year) - 6, int(datetime.now().year) + 1)]

    def secure_input(self, *args):
        proibidos = ['--', ';', '.', 'select', 'delete', 'update', 'from', 'insert', 'table', '*', "''", "/*", "'*\'", "'\'"]
        for caracter in proibidos:
            for entrada in args:
                entrada.lower()
                if caracter in entrada:
                    return False
        return True

    def pega_dados_por_ano(self, coluna, order_by='', where='', anos=''):
        try:
            if self.secure_input(coluna, order_by, where):
                args = []
                select = f"SELECT ag.{coluna}"
                _from = f'FROM graduacoes g'
                join = f'JOIN alunos_graduacao ag ON g.numeroUSP = ag.numeroUSP'
                group_by = f'GROUP BY ag.{coluna}'

                if where:
                    args = [where,]
                    where = "WHERE g.nomeCurso = %s"

                if order_by:
                    order_by = f"ORDER BY {order_by}"
                sum = []
                for ano in anos:
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
                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except:
            self.cursor.close()
            raise Exception("Não foi possivel realizar a query") 
        
    def conta_pessoa_por_categoria(self, tabela, situacao):
        try:
            if self.secure_input(tabela, situacao):
                self.cursor.execute(f"SELECT COUNT(*) FROM {tabela} WHERE situacaoCurso = %s", [situacao])
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except:
            raise Exception("Não foi possivel realizar a query") 
