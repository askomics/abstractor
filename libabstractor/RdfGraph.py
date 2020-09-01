import rdflib
import re


class RdfGraph(object):
    """Summary

    Attributes
    ----------
    gprefix : rdflib.namespace.Namespace
        Rdf prefix for askomics
    graph : rdflib.Graph
        The RDF graph
    """

    def __init__(self, namespace_internal):
        """init

        Parameters
        ----------
        namespace_internal : str
            AskOmics internal namespace
        """
        self.namespace_internal = rdflib.namespace.Namespace(namespace_internal)
        self.graph = rdflib.Graph()

        self.graph.bind('askomics', namespace_internal)
        self.prov = rdflib.Namespace('http://www.w3.org/ns/prov#')

    def check_entity(self, entity):
        """Check if entity is correct (not rdf rdfs owl or virtuoso thing)

        Parameters
        ----------
        entity : str
            Entity uri to check

        Returns
        -------
        bool
            True if entity is a true one
        """
        excluded_namespaces = (
            "http://www.w3.org",
            "http://www.openlinksw.com"
        )

        if entity.lower().startswith(excluded_namespaces):
            return False
        return True

    def add_location(self, location):
        """Add location of the data

        Parameters
        ----------
        location : str
            URL of distant endpoint
        """
        self.graph.add((rdflib.BNode("graph"), self.prov.atLocation, rdflib.Literal(location)))

    def add_entities(self, sparql_result):
        """Add entities

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        for result in sparql_result:
            if self.check_entity(result["entity"]):
                self.graph.add((rdflib.URIRef(result["entity"]), rdflib.RDF.type, self.namespace_internal["entity"]))
                self.graph.add((rdflib.URIRef(result["entity"]), rdflib.RDF.type, self.namespace_internal["startPoint"]))
                self.graph.add((rdflib.URIRef(result["entity"]), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(result["entity"]), self.namespace_internal["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(result["entity"]), rdflib.RDFS.label, rdflib.Literal(self.get_label(result["entity"]))))

    def add_relation(self, source_entity, relation, target_entity):
        """Add a relation

        Parameters
        ----------
        source_entity : str
            Source URI
        relation : str
            Relation URI
        target_entity : str
            Target URI
        """
        # Relation
        if self.check_entity(relation):
            self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, rdflib.OWL.ObjectProperty))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, self.namespace_internal["AskomicsRelation"]))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.label, rdflib.Literal(self.get_label(relation))))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.domain, rdflib.URIRef(source_entity)))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.range, rdflib.URIRef(target_entity)))

    def add_attribute(self, entity, attribute, decimal=True):
        """Add attribute

        Parameters
        ----------
        entity : str
            Source URI
        attribute : str
            Attribue URI
        """
        if self.check_entity(entity):
            self.graph.add((rdflib.URIRef(attribute), rdflib.RDF.type, rdflib.OWL.DatatypeProperty))
            self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.label, rdflib.Literal(self.get_label(attribute))))
            self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.domain, rdflib.URIRef(entity)))
            self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.range, rdflib.XSD.decimal if decimal else rdflib.XSD.string))

    def add_entities_and_relations(self, sparql_result):
        """Add entities and relation in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        entities = []

        # Entities and relations
        for result in sparql_result:
            source_entity = result["source_entity"]
            target_entity = result["target_entity"]
            relation = result["relation"]
            mother_source = result["mother_source"] if "mother_source" in result else None
            mother_target = result["mother_target"] if "mother_target" in result else None

            # Source entity
            if self.check_entity(source_entity) and source_entity not in entities:
                entities.append(source_entity)
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, self.namespace_internal["entity"]))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, self.namespace_internal["startPoint"]))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(source_entity), self.namespace_internal["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDFS.label, rdflib.Literal(self.get_label(source_entity))))
                if mother_source:
                    self.graph.add((rdflib.URIRef(source_entity), rdflib.RDFS.subClassOf, rdflib.URIRef(mother_source)))

            # Target entity
            if self.check_entity(target_entity) and target_entity not in entities:
                entities.append(target_entity)
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, self.namespace_internal["entity"]))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, self.namespace_internal["startPoint"]))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(target_entity), self.namespace_internal["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDFS.label, rdflib.Literal(self.get_label(target_entity))))
                if mother_target:
                    self.graph.add((rdflib.URIRef(source_entity), rdflib.RDFS.subClassOf, rdflib.URIRef(mother_target)))

            # Relation
            if self.check_entity(relation):
                self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, rdflib.OWL.ObjectProperty))
                self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, self.namespace_internal["AskomicsRelation"]))
                self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.label, rdflib.Literal(self.get_label(relation))))
                self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.domain, rdflib.URIRef(source_entity)))
                self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.range, rdflib.URIRef(target_entity)))

    def add_decimal_attributes(self, sparql_result):
        """Add decimal  in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        for result in sparql_result:
            entity = result["entity"]
            attribute = result["attribute"]

            if self.check_entity(entity):
                self.graph.add((rdflib.URIRef(attribute), rdflib.RDF.type, rdflib.OWL.DatatypeProperty))
                self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.label, rdflib.Literal(self.get_label(attribute))))
                self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.domain, rdflib.URIRef(entity)))
                self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.range, rdflib.XSD.decimal))

    def add_text_attributes(self, sparql_result):
        """Add text  in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        for result in sparql_result:
            entity = result["entity"]
            attribute = result["attribute"]

            if self.check_entity(entity):
                if attribute == "http://www.w3.org/2000/01/rdf-schema#label":
                    self.graph.remove((rdflib.URIRef(entity), self.namespace_internal["instancesHaveNoLabels"], rdflib.Literal(True)))
                else:
                    self.graph.add((rdflib.URIRef(attribute), rdflib.RDF.type, rdflib.OWL.DatatypeProperty))
                    self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.label, rdflib.Literal(self.get_label(attribute))))
                    self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.domain, rdflib.URIRef(entity)))
                    self.graph.add((rdflib.URIRef(attribute), rdflib.RDFS.range, rdflib.XSD.string))

    def get_label(self, uri):
        """Get a label from an URI

        Parameters
        ----------
        uri : string
            URi to get a label

        Returns
        -------
        string
            Label
        """
        return self.uncamel(uri.split("/")[-1].split("#")[-1].replace("_", " "))

    @staticmethod
    def uncamel(string):
        """Insert space beween camelcased words

        Parameters
        ----------
        string : str
            CamelCased string

        Returns
        -------
        str
            Uncamel Cased string
        """
        re_outer = re.compile(r'([^A-Z ])([A-Z])')
        re_inner = re.compile(r'\b[A-Z]+(?=[A-Z][a-z])')
        uncameled = re_inner.sub(r'\g<0> ', re_outer.sub(r'\1 \2', string))
        if uncameled[0].islower():
            return uncameled.lower()
        return uncameled
