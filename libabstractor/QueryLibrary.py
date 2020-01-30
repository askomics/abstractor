import textwrap


class QueryLibrary(object):
    """SPARQL methods"""

    def __init__(self):
        """init"""
        pass

    @property
    def entities_and_relations(self):
        """Sparql query to get entities and relations

        Returns
        -------
        str
            SPARQL query
        """
        return textwrap.dedent('''
        SELECT DISTINCT ?source_entity ?relation ?target_entity
        WHERE {
            # Get entities
            ?instance_of_source a ?source_entity .
            ?instance_of_target a ?target_entity .
            # Relations
            ?instance_of_source ?relation ?instance_of_target .
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
        SELECT DISTINCT ?source_entity ?relation ?target_entity
        WHERE {{
            ?source_entity a owl:Class .
            ?source_entity rdfs:isDefinedBy <{ontology}> .

            ?target_entity a owl:Class .
            ?target_entity rdfs:isDefinedBy <{ontology}> .

            ?relation a owl:ObjectProperty .
            ?relation rdfs:domain ?source_entity .
            ?relation rdfs:range ?target_entity .
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
            ?attribute rdfs:domain ?entity .
            ?attribute rdfs:range ?range .
            VALUES ?range {{ xsd:float xsd:int }} .
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
            ?attribute rdfs:domain ?entity .
            ?attribute rdfs:range ?range .
            VALUES ?range {{ xsd:string }} .
        }}
        '''.format(ontology=ontology))
