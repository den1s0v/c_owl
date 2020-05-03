# test_upd_onto.py

from upd_onto import *



from upd_onto import *
import shutil


# c:\D\Нинь\учёба\09s\reasoning\onto-work\c_owl\upd-ontology-test.rdf
# onto_path.append(r"c:\D\Нинь\учёба\09s\reasoning\onto-work\c_owl")


onto_path.append(r"onto")


# Пути неверные! См. ipynb в \Dev\ML_exp\owlready\TestUpdOnto.ipynb
ontology_path = "onto/upd-ontology-test.rdf"
ontology_file = "upd-ontology-test.rdf"

onto = get_ontology(ontology_file)
onto.load()

list(onto.individuals())

wr_onto = AugmentingOntology(onto, no_init=1)
wr_onto.init(verbose=1)

with onto:
    r = """

        Referenceable(?x), Referenceable(?y), DifferentFrom(?x, ?y) -> UNLINK_friend(?x, ?y)
    """
    Imp().set_as_rule(r)

with onto:
    r = """

        Referenceable(?x), IRI(?x, "d") -> DESTROY_INSTANCE(?x), CREATE(INSTANCE , "Referenceable{neighbour=a; friend=b}")
    """
    Imp().set_as_rule(r)

list(onto.individuals())

wr_onto.sync()

shutil.copyfile(ontology_path, ontology_path.replace(".", "_backup."))

ontology_file2 = ontology_path.replace(".", "_ext.")

onto.save(file=ontology_file2, format='rdfxml')
print("Saved RDF file: {} !".format(ontology_file2))












