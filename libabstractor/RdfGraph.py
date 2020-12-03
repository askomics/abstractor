import re
from datetime import datetime

import rdflib


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
        self.graph.bind('owl', "http://www.w3.org/2002/07/owl#")
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
            "http://www.openlinksw.com",
            self.namespace_internal[""],
            "http://biohackathon.org/resource/faldo"
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
        self.graph.add((rdflib.BNode("graph"), rdflib.RDF.type, self.prov["Entity"]))
        self.graph.add((rdflib.BNode("graph"), self.prov.atLocation, rdflib.Literal(location)))
        self.graph.add((rdflib.BNode("graph"), self.prov.generatedAtTime, rdflib.Literal(datetime.now())))
        self.graph.add((rdflib.BNode("graph"), self.prov.wasGeneratedBy, rdflib.URIRef("https://github.com/askomics/abstractor")))

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

    def add_entities_askomics(self, sparql_result):
        """Add entities (Askomics definition) in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        # ?entity ?startPoint ?faldoObject
        for result in sparql_result:
            entity = result["entity"]
            label = result["label"]
            start_point = bool(result["startPoint"].lower() in ['true', '1'])
            faldo_object = bool(result["faldoObject"].lower() in ['true', '1'])

            self.graph.add((rdflib.URIRef(entity), rdflib.RDF.type, self.namespace_internal["entity"]))
            self.graph.add((rdflib.URIRef(entity), rdflib.RDF.type, rdflib.OWL.Class))
            self.graph.add((rdflib.URIRef(entity), rdflib.RDFS.label, rdflib.Literal(label)))
            if start_point:
                self.graph.add((rdflib.URIRef(entity), rdflib.RDF.type, self.namespace_internal["startPoint"]))
            if faldo_object:
                self.graph.add((rdflib.URIRef(entity), rdflib.RDF.type, self.namespace_internal["faldo"]))

    def add_relations_askomics(self, sparql_result):
        """Add entities (Askomics definition) in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        # ?entitySource ?entityTarget ?relation
        for result in sparql_result:
            entity_source = result["entitySource"]
            entity_target = result["entityTarget"]
            relation = result["relation"]
            label = result["label"]

            self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, self.namespace_internal["AskomicsRelation"]))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDF.type, rdflib.OWL.ObjectProperty))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.domain, rdflib.URIRef(entity_source)))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.range, rdflib.URIRef(entity_target)))
            self.graph.add((rdflib.URIRef(relation), rdflib.RDFS.label, rdflib.Literal(label)))

    def add_attributes_askomics(self, sparql_result):
        """Add attributes (Askomics definition) in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        # ?entity ?att ?label ?range ?faldoStart ?faldoEnd
        for result in sparql_result:
            entity = result["entity"]
            att = result["att"]
            label = result["label"]
            range = result["range"]
            faldo_start = bool(result["faldoStart"].lower() in ['true', '1'])
            faldo_end = bool(result["faldoEnd"].lower() in ['true', '1'])

            self.graph.add((rdflib.URIRef(att), rdflib.RDF.type, rdflib.OWL.DatatypeProperty))
            self.graph.add((rdflib.URIRef(att), rdflib.RDFS.domain, rdflib.URIRef(entity)))
            self.graph.add((rdflib.URIRef(att), rdflib.RDFS.range, rdflib.URIRef(range)))
            self.graph.add((rdflib.URIRef(att), rdflib.RDFS.label, rdflib.Literal(label)))
            if faldo_start:
                self.graph.add((rdflib.URIRef(att), rdflib.RDF.type, self.namespace_internal["faldoStart"]))
            if faldo_end:
                self.graph.add((rdflib.URIRef(att), rdflib.RDF.type, self.namespace_internal["faldoEnd"]))

    def add_categories_askomics(self, sparql_result):
        """Add categories (Askomics definition) in the rdf graph

        Parameters
        ----------
        sparql_result : list
            Sparql result
        """
        categories = []
        # ?cat ?label ?entity ?catValueType ?valueCategory valueCategoryLabel ?faldoReference
        for result in sparql_result:
            entity = result["entity"]
            cat = result["cat"]
            label = result["label"]
            category_type = result["catValueType"]
            category_value = result["valueCategory"]
            category_value_label = result["valueCategoryLabel"]
            category_value_type = result["valueCategoryType"]
            faldo_ref = bool(result["faldoReference"].lower() in ['true', '1'])

            if cat not in categories:
                categories.append(cat)
                self.graph.add((rdflib.URIRef(cat), rdflib.RDF.type, self.namespace_internal["AskomicsCategory"]))
                self.graph.add((rdflib.URIRef(cat), rdflib.RDF.type, rdflib.OWL.ObjectProperty))
                self.graph.add((rdflib.URIRef(cat), rdflib.RDFS.label, rdflib.Literal(label)))
                self.graph.add((rdflib.URIRef(cat), rdflib.RDFS.domain, rdflib.URIRef(entity)))
                self.graph.add((rdflib.URIRef(cat), rdflib.RDFS.range, rdflib.URIRef(category_type)))
                if faldo_ref:
                    self.graph.add((rdflib.URIRef(cat), rdflib.RDF.type, self.namespace_internal["faldoReference"]))

            self.graph.add((rdflib.URIRef(category_type), self.namespace_internal["category"], rdflib.URIRef(category_value)))
            self.graph.add((rdflib.URIRef(category_value), rdflib.RDFS.label, rdflib.Literal(category_value_label)))
            self.graph.add((rdflib.URIRef(category_value), rdflib.RDF.type, rdflib.URIRef(category_value_type)))

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
