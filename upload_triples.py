# Триплеты - пример разбора программы
triples = [
 (':Algorithm_2@root', 'rdf:type', ':Algorithm'),
 (':Algorithm_2@root', ':hasFunc', ':main()_1@3:6'),
 (':main()_1@3:6', 'rdf:type', ':Function'),
 (':main()_1@3:6', ':hasName', ':main'),
 (':main()_1@3:6', ':hasBody', ':Seq_13@5'),
 (':Seq_13@5', ':hasFirstSt', ':for(;;)_1@5:2'),
 (':Seq_13@5', ':hasLastSt', ':for(;;)_1@5:2'),
 (':Seq_13@5', ':hasSubStmt', ':for(;;)_1@5:2'),
 (':for(;;)_1@5:2', 'rdf:type', ':FOR_st'),
 (':for(;;)_1@5:2', ':hasFORInit', ':empty_2@5:2'),
 (':empty_2@5:2', 'rdf:type', ':Empty_st'),
 (':for(;;)_1@5:2', ':hasFORUpdate', ':empty_3@5:2'),
 (':empty_3@5:2', 'rdf:type', ':Empty_st'),
 (':for(;;)_1@5:2', ':hasBody', ':Seq_12@7+'),
 (':Seq_12@7+', ':hasFirstSt', ':call~st_3()_1@7:9'),
 (':Seq_12@7+', ':hasLastSt', ':if(1)_2@8:9'),
 (':Seq_12@7+', ':hasSubStmt', ':call~st_3()_1@7:9'),
 (':call~st_3()_1@7:9', 'rdf:type', ':FuncCall'),
 (':Seq_12@7+', ':hasSubStmt', ':if(1)_2@8:9'),
 (':if(1)_2@8:9', 'rdf:type', ':IF_st'),
 (':if(1)_2@8:9', ':hasThenBranch', ':if(0)_1@9:13'),
 (':if(0)_1@9:13', 'rdf:type', ':IF_st'),
 (':if(0)_1@9:13', ':hasThenBranch', ':Seq_11@11+'),
 (':Seq_11@11+', ':hasFirstSt', ':call~do_9()_1@11:17'),
 (':Seq_11@11+', ':hasLastSt', ':break-FOR_1@13:17'),
 (':Seq_11@11+', ':hasSubStmt', ':call~do_9()_1@11:17'),
 (':call~do_9()_1@11:17', 'rdf:type', ':FuncCall'),
 (':Seq_11@11+', ':hasSubStmt', ':call~do_10()_1@12:17'),
 (':call~do_10()_1@12:17', 'rdf:type', ':FuncCall'),
 (':call~do_9()_1@11:17', ':hasNextSt', ':call~do_10()_1@12:17'),
 (':Seq_11@11+', ':hasSubStmt', ':break-FOR_1@13:17'),
 (':break-FOR_1@13:17', 'rdf:type', ':BREAK_st'),
 (':break-FOR_1@13:17', ':breaksLoop', ':for(;;)_1@5:2'),
 (':call~do_10()_1@12:17', ':hasNextSt', ':break-FOR_1@13:17'),
 (':if(0)_1@9:13', ':hasElseBranch', ':continue-FOR_1@16:13'),
 (':continue-FOR_1@16:13', 'rdf:type', ':CONTINUE_st'),
 (':continue-FOR_1@16:13', ':continuesLoop', ':for(;;)_1@5:2'),
 (':call~st_3()_1@7:9', ':hasNextSt', ':if(1)_2@8:9'),
 (':Algorithm_2@root', ':hasFunc', ':my_f()_1@20:6'),
 (':my_f()_1@20:6', 'rdf:type', ':Function'),
 (':my_f()_1@20:6', ':hasName', ':my_f'),
 (':my_f()_1@20:6', ':hasBody', ':Seq_15@22+'),
 (':Seq_15@22+', ':hasFirstSt', ':call~see_help()_1@22:5'),
 (':Seq_15@22+', ':hasLastSt', ':return_1@25:5'),
 (':Seq_15@22+', ':hasSubStmt', ':call~see_help()_1@22:5'),
 (':call~see_help()_1@22:5', 'rdf:type', ':FuncCall'),
 (':Seq_15@22+', ':hasSubStmt', ':if(1)_3@23:5'),
 (':if(1)_3@23:5', 'rdf:type', ':IF_st'),
 (':if(1)_3@23:5', ':hasThenBranch', ':call~my_f()_1@24:9'),
 (':call~my_f()_1@24:9', 'rdf:type', ':FuncCall'),
 (':call~my_f()_1@24:9', ':callOf', ':my_f()_1@20:6'),
 (':call~see_help()_1@22:5', ':hasNextSt', ':if(1)_3@23:5'),
 (':Seq_15@22+', ':hasSubStmt', ':return_1@25:5'),
 (':return_1@25:5', 'rdf:type', ':RETURN_st'),
 (':return_1@25:5', ':returnsFrom', ':my_f()_1@20:6'),
 (':if(1)_3@23:5', ':hasNextSt', ':return_1@25:5')]


# Формирование текста INSERT-запроса из одонго триплета
def triple_to_sparql_insert(triple, prefix_str=""):
    s = """INSERT DATA
	{
	%s %s %s .
	}""" % triple
    return prefix_str + s


# Используем наш базовый префикс онтологии
prefix_str = """
BASE <http://vstu.ru/poas/se/c_schema_2020-01#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

"""

# Пробуем на одном триплете
q = triple_to_sparql_insert(triples[0], prefix_str)

print(q)
# >>
# BASE <http://vstu.ru/poas/se/c_schema_2020-01#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

# INSERT DATA
# {
# :Algorithm_2@root rdf:type :Algorithm .
# }



# Далее должен быть цикл загрузки всех триплетов ...

import stardog

conn_details = {
  'endpoint': 'http://localhost:5820',
  'username': 'admin',
  'password': 'admin'
}

with stardog.Admin(**conn_details) as admin:

	with stardog.Connection('с_owl', **conn_details) as conn:

		for trpl in triples:
			q = triple_to_sparql_insert(trpl, prefix_str)
			print('Go...', end='')
			# как называется метод для отправки запросов SPARQL UPDATE, я не в курсе: проверь. Но не `select` - точно.
			results = conn.update(q, reasoning=False)
			print(' done!')

			# pprint(results)


# теперь можно проверять содержимое базы ...