import textwrap


class QueryLibrary(object):
    """SPARQL methods"""
    askomics_ns = "http://askomics.org/internal/"

    def __init__(self):
        """init"""
        pass

    @property
    def get_entities(self):
        """Sparql query to get all entities

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entity
        WHERE {
            ?instance a ?entity .
        }
        ''')

    def get_relation_for_entity(self, entity):
        """Sparql query to get all relations of an entity

        Parameters
        ----------
        entity : string
            The source entity

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?relation ?target_entity
        WHERE {{
            <{}> ?relation ?target_entity .
            ?instance_of_target a ?target_entity .
        }}
        '''.format(entity))

    def get_numeric_attribute_for_entity(self, entity):
        """Sparql query to get all attribute of an entity

        Parameters
        ----------
        entity : string
            The source entity

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?attribute
        WHERE {{
            # Get entities
            ?instance_of_entity a <{}> .
            # Attributes
            ?instance_of_entity ?attribute ?value .
            FILTER (isNumeric(?value))
        }}
        '''.format(entity))

    def get_text_attribute_for_entity(self, entity):
        """Sparql query to get all text attribute of an entity

        Parameters
        ----------
        entity : string
            The source entity

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?attribute
        WHERE {{
            # Get entities
            ?instance_of_entity a <{}> .
            # Attributes
            ?instance_of_entity ?attribute ?value .
            FILTER (isLiteral(?value))
            FILTER (!isNumeric(?value))
        }}
        '''.format(entity))

    @property
    def entities_and_relations(self):
        """Sparql query to get entities and relations

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?source_entity ?relation ?target_entity ?mother_source ?mother_target
        WHERE {
            # Get entities
            ?instance_of_source a ?source_entity .
            ?instance_of_target a ?target_entity .
            # Relations
            ?instance_of_source ?relation ?instance_of_target .

            OPTIONAL {{
                ?source_entity rdfs:subClassOf ?mother_source .
            }}
            OPTIONAL {{
                ?target_entity rdfs:subClassOf ?mother_target .
            }}
        }
        ''')

    @property
    def entities_askomics(self):
        """Sparql query to get entities and relations

        Returns
        -------
        str
            SPARQL query
        """

        return textwrap.dedent('''
        SELECT DISTINCT ?entity ?label ?startPoint ?faldoObject
        WHERE {
            # Get entities
            ?entity a <''' + self.askomics_ns + '''entity> .
            ?entity rdfs:label ?label .
            bind( exists { ?entity a <''' + self.askomics_ns + '''startPoint> } as ?startPoint )
            bind( exists { ?entity a <''' + self.askomics_ns + '''faldo> } as ?faldoObject )
        }
        ''')

    @property
    def relations_askomics(self):
        """Sparql query to get entities and relations

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entitySource ?entityTarget ?relation ?label
        WHERE {
            # Get entities

            ?entitySource a <''' + self.askomics_ns + '''entity> .
            ?entityTarget a <''' + self.askomics_ns + '''entity> .

            ?relation rdfs:domain ?entitySource  .
            ?relation rdfs:range ?entityTarget  .
            ?relation rdfs:label ?label .
        }
        ''')

    @property
    def attributes_askomics(self):
        """Sparql query to get entities and numeric attributes

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entity ?att ?label ?range ?faldoStart ?faldoEnd
        WHERE {
            ?entity a <''' + self.askomics_ns + '''entity> .
            ?att rdfs:domain ?entity  .
            ?att rdfs:range ?range  .
            ?att rdfs:label ?label .
            filter( strstarts(str(?range), "http://www.w3.org/2001/XMLSchema#") )
            bind( exists { ?att a <''' + self.askomics_ns + '''faldoStart> } as ?faldoStart )
            bind( exists { ?att a <''' + self.askomics_ns + '''faldoEnd> } as ?faldoEnd )
        }
        ''')

    @property
    def categories_askomics(self):
        """Sparql query to get Askomics categories attributes

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?cat ?label ?entity ?catValueType ?valueCategory ?valueCategoryLabel ?valueCategoryType ?faldoReference
        WHERE {
            ?cat a <''' + self.askomics_ns + '''AskomicsCategory> .
            ?cat rdfs:domain ?entity  .
            ?cat rdfs:range ?catValueType  .
            ?cat rdfs:label ?label .

            ?catValueType <''' + self.askomics_ns + '''category> ?valueCategory.
            ?valueCategory rdfs:label ?valueCategoryLabel .
            ?valueCategory a ?valueCategoryType .

            bind( exists { ?cat a <''' + self.askomics_ns + '''faldoReference> } as ?faldoReference )
        }
        ''')

    @property
    def entities_and_numeric_attributes(self):
        """Sparql query to get entities and numeric attributes

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entity ?attribute
        WHERE {
            # Get entities
            ?instance_of_entity a ?entity .
            # Attributes
            ?instance_of_entity ?attribute ?value .
            FILTER (isNumeric(?value))
        }
        ''')

    @property
    def entities_and_text_attributes(self):
        """Sparql query to get entities and text attributes

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entity ?attribute
        WHERE {
            # Get entities
            ?instance_of_entity a ?entity .
            # Attributes
            ?instance_of_entity ?attribute ?value .
            FILTER (isLiteral(?value))
            FILTER (!isNumeric(?value))
        }
        ''')

    @property
    def ontologies(self):
        """Sparql query to get ontologies

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?ontology
        WHERE {
            ?ontology a owl:Ontology .
            ?entity a owl:Class .
            ?relation a owl:ObjectProperty .
            ?attribute a owl:DatatypeProperty .
            ?entity rdfs:isDefinedBy ?ontology .
            ?relation rdfs:isDefinedBy ?ontology .
            ?attribute rdfs:isDefinedBy ?ontology .
        }
        ''')

    @staticmethod
    def entities_and_relations_with_ontology(ontology):
        """Sparql query to get entities and relations

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?source_entity ?relation ?target_entity ?mother_source ?mother_target
        WHERE {{
            ?source_entity a owl:Class .
            ?source_entity rdfs:isDefinedBy <{ontology}> .

            ?target_entity a owl:Class .
            ?target_entity rdfs:isDefinedBy <{ontology}> .

            ?relation a owl:ObjectProperty .
            ?relation rdfs:range ?target_entity .
            {{
                ?relation rdfs:domain/(owl:unionOf/(rdf:rest*)/rdf:first) ?source_entity .
            }} UNION {{
                ?relation rdfs:domain ?source_entity .
            }}
            OPTIONAL {{
                ?source_entity rdfs:subClassOf ?mother_source .
            }}
            OPTIONAL {{
                ?target_entity rdfs:subClassOf ?mother_target .
            }}
        }}
        '''.format(ontology=ontology))

    @staticmethod
    def entities_and_numeric_attributes_with_ontology(ontology):
        """Sparql query to get entities and numeric attributes

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entity ?attribute
        WHERE {{
            # Entity
            ?entity a owl:Class .
            ?entity rdfs:isDefinedBy <{ontology}> .
            # Attribute
            ?attribute a owl:DatatypeProperty .
            ?attribute rdfs:range ?range .
            VALUES ?range {{ xsd:float xsd:int }} .
            {{
                ?attribute rdfs:domain/(owl:unionOf/(rdf:rest*)/rdf:first) ?entity .
            }} UNION {{
                ?attribute rdfs:domain ?entity .
            }}
        }}
        '''.format(ontology=ontology))

    @staticmethod
    def entities_and_text_attributes_with_ontology(ontology):
        """Sparql query to get entities and numeric attributes

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?entity ?attribute
        WHERE {{
            # Entity
            ?entity a owl:Class .
            ?entity rdfs:isDefinedBy <{ontology}> .
            # Attribute
            ?attribute a owl:DatatypeProperty .
            ?attribute rdfs:range ?range .
            VALUES ?range {{ xsd:string }} .
            {{
                ?attribute rdfs:domain/(owl:unionOf/(rdf:rest*)/rdf:first) ?entity .
            }} UNION {{
                ?attribute rdfs:domain ?entity .
            }}
        }}
        '''.format(ontology=ontology))
