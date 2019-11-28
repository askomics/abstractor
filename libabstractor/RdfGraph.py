import rdflib
import re


class RdfGraph(object):
    """Summary

    Attributes
    ----------
    endpoint_prefix : str
        Prefix of external endpoind
    gprefix : rdflib.namespace.Namespace
        Rdf prefix for askomics
    graph : rdflib.Graph
        The RDF graph
    """

    def __init__(self, askomics_prefix, endpoint_prefix, endpoint_name):
        """init

        Parameters
        ----------
        askomics_prefix : str
            AskOmics prefix
        endpoint_prefix : str
            External endpoint prefix
        endpoint_name : str
            Endpoint name
        """
        self.gprefix = rdflib.namespace.Namespace(askomics_prefix)
        self.endpoint_prefix = endpoint_prefix
        self.graph = rdflib.Graph()

        self.graph.bind('', askomics_prefix)
        self.graph.bind(endpoint_name, endpoint_prefix)

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
            if source_entity.startswith(self.endpoint_prefix) and source_entity not in entities:
                entities.append(source_entity)
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, self.gprefix["entity"]))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, self.gprefix["startPoint"]))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(source_entity), self.gprefix["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(source_entity), rdflib.RDFS.label, rdflib.Literal(self.get_label(source_entity))))

            # Target entity
            if target_entity.startswith(self.endpoint_prefix) and target_entity not in entities:
                entities.append(target_entity)
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, self.gprefix["entity"]))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, self.gprefix["startPoint"]))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDF.type, rdflib.OWL.Class))
                self.graph.add((rdflib.URIRef(target_entity), self.gprefix["instancesHaveNoLabels"], rdflib.Literal(True)))
                self.graph.add((rdflib.URIRef(target_entity), rdflib.RDFS.label, rdflib.Literal(self.get_label(target_entity))))

            # Relation
            if relation.startswith(self.endpoint_prefix):
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

            if entity.startswith(self.endpoint_prefix) and attribute.startswith(self.endpoint_prefix):
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

            if entity.startswith(self.endpoint_prefix) and attribute.startswith(self.endpoint_prefix):

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
