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
