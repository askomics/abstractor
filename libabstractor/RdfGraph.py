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

    def __init__(self, askomics_prefix):
        """init

        Parameters
        ----------
        askomics_prefix : str
            AskOmics prefix
        """
        self.gprefix = rdflib.namespace.Namespace(askomics_prefix)
        self.graph = rdflib.Graph()

        self.graph.bind('askomics', askomics_prefix)

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
        excluded_prefixes = (
            "http://www.w3.org/2002/07/owl#",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "http://www.w3.org/2000/01/rdf-schema#",
            "http://www.openlinksw.com/schemas/virtrdf#",
            "http://www.w3.org/ns/sparql-service-description#"
        )

        if entity.lower().startswith(excluded_prefixes):
            return False
        return True

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

            # Source entity
            if self.check_entity(source_entity) and source_entity not in entities:
                entities.append(source_entity)
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, self.gprefix["entity"]))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, self.gprefix["startPoint"]))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(source_entity), self.gprefix["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDFS.label, rdflib.Literal(self.get_label(source_entity))))

            # Target entity
            if self.check_entity(target_entity) and target_entity not in entities:
                entities.append(target_entity)
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, self.gprefix["entity"]))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, self.gprefix["startPoint"]))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(target_entity), self.gprefix["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDFS.label, rdflib.Literal(self.get_label(target_entity))))

            # Relation
            if self.check_entity(relation):
                self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, rdflib.OWL.ObjectProperty))
                self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, self.gprefix["AskomicsRelation"]))
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

            if self.check_entity(entity) and self.check_entity(attribute):
                """<FRESHLY_INSERTED>"""
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

            if self.check_entity(entity) and self.check_entity(attribute):

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
