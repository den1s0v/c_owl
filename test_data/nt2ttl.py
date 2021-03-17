import rdflib

file_in = "jena_output.n3"
file_out = "jena_output.ttl"

g = rdflib.Graph()

g.bind("my", "http://vstu.ru/poas/ctrl_structs_2020-05_v1#")
g.bind("owl", "http://www.w3.org/2002/07/owl#")

print("reading ... ", end='')
g.parse(location=file_in, format="n3")
print("done")
print("saving ... ", end='')
g.serialize(file_out, format="turtle")
print("done.")
