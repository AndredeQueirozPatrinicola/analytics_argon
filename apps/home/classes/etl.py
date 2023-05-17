from django.db import connections

from datetime import datetime


class Etl:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()
        self.anos = [i for i in range(
            int(datetime.now().year) - 6, int(datetime.now().year) + 1)]

    def secure_input(self, *args):
        proibidos = ['--', ';', '.', 'select', 'delete', 'update',
                     'from', 'insert', 'table', '*', "''", "/*", "'*\'", "'\'"]
        for caracter in proibidos:
            for entrada in args:
                str(entrada).lower()
                if caracter in entrada:
                    return False
        return True

    def pega_dados_por_ano(self, table, coluna, pos="",coluna_datas=[], order_by='', where='', anos=''):
        try:
            if self.secure_input(coluna, order_by, where, anos):
                args = []
                select = f"SELECT p.{coluna}"
                _from = f'FROM {table} g'
                join = f'JOIN pessoas p ON g.numero_usp = p.numero_usp'
                group_by = f'GROUP BY p.{coluna}'

                if where:
                    args.append(list(where.values())[0])
                    where = f"WHERE {list(where.keys())[0]} = " + "%s"

                if order_by:
                    order_by = f"ORDER BY {order_by}"

                sum = []
                for ano in anos:
                    if pos:
                        sum.append(
                            f"""
                                , SUM(
                                    CASE WHEN (
                                        (YEAR({coluna_datas[0]}) <= {ano}) AND 
                                        (
                                            (YEAR({coluna_datas[1]}) >= {ano}) OR 
                                            (
                                                ({coluna_datas[1]} IS NULL) AND 
                                                (YEAR({coluna_datas[2]}) >= {ano} )
                                            )
                                        )
                                    ) THEN 1 ELSE 0 END) AS '{ano}'
                            """
                        )
                    else:
                        sum.append(
                            f", SUM(CASE WHEN ({ano} >= YEAR({coluna_datas[0]})) AND ({ano} <= YEAR({coluna_datas[1]}) OR {coluna_datas[1]} IS NULL) THEN 1 ELSE 0 END) AS '{ano}'")
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
        except Exception as e:
            self.cursor.close()
            raise Exception("Não foi possivel realizar a query:" + e)

    def conta_pessoa_por_categoria(self, tabela, situacao):
        try:
            if self.secure_input(tabela, situacao):
                self.cursor.execute(
                    f"SELECT COUNT(*) FROM {tabela} WHERE situacaoCurso = %s", [situacao])
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)

    def relaciona_dados_em_determinado_ano(self, *args, **kwargs):
        try:
            if self.secure_input(args):
                args = [kwargs.get('data_inicio'), kwargs.get('data_fim')]
                select = f"""
                            SELECT 
                                y.{kwargs.get('column_1')},
                                y.{kwargs.get('column_2')},
                                COUNT(*)
                            FROM {kwargs.get('table_1')} x
                        """
                join = f"JOIN {kwargs.get('table_2')} y ON x.numero_usp = y.numero_usp"
                where = """
                                WHERE 
                                YEAR(x.data_inicio_vinculo) >= %s AND YEAR(x.data_fim_vinculo) <= %s
                                OR YEAR(x.data_fim_vinculo) IS NULL
                            """
                if kwargs.get('departamento'):
                    where = where + "AND x.nome_curso = %s"
                    args.append(kwargs.get('departamento'))

                group_by = f"GROUP BY y.{kwargs.get('column_1')}, y.{kwargs.get('column_2')}"
                order_by = f"ORDER BY y.{kwargs.get('column_1')}"
                
                query = f"""
                            {select}
                            {join}
                            {where}
                            {group_by}
                            {order_by}
                        """

                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)
        
    def soma_por_ano(self, table, anos, coluna_ano, coluna_select="", where = ""):
        try:

            if self.secure_input(anos):
                args = []
                group_by = ""

                sum = []
                for ano in anos:
                    if ano == anos[0]:
                        sum.append(
                            f"SUM(CASE WHEN YEAR({coluna_ano}) = {ano} THEN 1 ELSE 0 END) as '{ano}'")
                    else:
                        sum.append(
                            f", SUM(CASE WHEN YEAR({coluna_ano}) = {ano} THEN 1 ELSE 0 END) as '{ano}'")
                sum = "".join(sum)

                if where:
                    args.append(list(where.values())[0])
                    where = f"WHERE {list(where.keys())[0]} = %s"

                if coluna_select:
                    group_by = f"GROUP BY {coluna_select} ORDER BY {coluna_select}"
                    coluna_select = f"{coluna_select}, "

                query = f"SELECT {coluna_select} {sum} FROM {table} {where} {group_by};"
                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)

    def group_by(self, *args, **kwargs):
        try:
            if self.secure_input():
                colunas_completas = ",".join(kwargs.get("columns"))
                tabela_1 = kwargs.get("tables")[0]
                tabela_2 = kwargs.get("tables")[1]
                ids = kwargs.get("ids")
                where_column = list(kwargs.get("condition").keys())[0]
                where_condition = kwargs.get("condition").get(where_column)
                group_by = ",".join(kwargs.get("group_by"))

                select_statement = f"SELECT {colunas_completas}" 
                from_statement = f"FROM {tabela_1} x" 
                join_statement = f"JOIN {tabela_2} y ON x.{ids} = y.{ids}" 
                where_statement = f"WHERE {where_column} in " + "(%s)" 
                group_by_statement = f"GROUP BY {group_by}" 
            
                args = [where_condition]

                if where := kwargs.get("where"):
                    args.append(where)
                    where_statement += "AND nome_departamento = %s "

                query = f"""
                            {select_statement}
                            {from_statement}
                            {join_statement}
                            {where_statement}
                            {group_by_statement}
                        """

                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)