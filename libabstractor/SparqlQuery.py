import logging
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlQuery(object):
    """SPARQL methods

    Attributes
    ----------
    prefix : TYPE
        Description
    prefixes : TYPE
        Description
    rdf_source : TYPE
        Description
    source : TYPE
        Description
    source_type : TYPE
        Description
    """

    def __init__(self, source, source_type):
        """Init

        Parameters
        ----------
        source : TYPE
            Description
        source_type : TYPE
            Description
        """
        self.source = source
        self.source_type = source_type
        self.prefixes = {
            "owl:": "http://www.w3.org/2002/07/owl#",
            "rdf:": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs:": "http://www.w3.org/2000/01/rdf-schema#",
            "dc:": "http://purl.org/dc/elements/1.1/",
            "prov:": "http://www.w3.org/ns/prov#",
            "xsd:": "http://www.w3.org/2001/XMLSchema#",
            "skos:": "http://www.w3.org/2004/02/skos/core#",
            "chebi:": "http://purl.obolibrary.org/obo/",
            "drugbankdrugs:": "http://wifo5-04.informatik.uni-mannheim.de/drugbank/resource/drugs/"
        }

        # if source is a file, load it in a rdflib graph
        self.rdf_source = None
        if self.source_type != "sparql":
            self.rdf_source = rdflib.Graph()
            self.rdf_source.parse(self.source, format=self.source_type)

    def get_sparl_prefix(self):
        """Get a SPARQL prefix string

        Returns
        -------
        str
            SPARQL prefix string
        """
        prefixes_string = ""
        for prefix, uri in self.prefixes.items():
            prefixes_string += "PREFIX {} <{}>\n".format(prefix, uri)

        return prefixes_string

    def get_ttl_prefix(self):
        """Get a turtle prefix string

        Returns
        -------
        str
            Turtle prefix string
        """
        prefixes_string = ""
        for prefix, uri in self.prefixes.items():
            prefixes_string += "@prefix {} <{}> .\n".format(prefix, uri)

        return prefixes_string

    def execute_sparql_query(self, query):
        """Execute query on a SPARQL endpoint

        Parameters
        ----------
        query : str
            The query

        Returns
        -------
        list
            results
        """
        endpoint = SPARQLWrapper(self.source)
        endpoint.setQuery(query)
        endpoint.setReturnFormat(JSON)
        return endpoint.query().convert()

    def execute_rdflib_query(self, query):
        """Execute query on a rdflib graph

        Parameters
        ----------
        query : str
            The query

        Returns
        -------
        list
            results
        """
        return self.rdf_source.query(query)

    def parse_sparql_results(self, json_results):
        """Parse result of sparql query

        Parameters
        ----------
        json_results : dict
            Query result

        Returns
        -------
        list
            Parsed results
        """
        try:
            data = []
            for row in json_results["results"]["bindings"]:
                row_dict = {}
                for key, value in row.items():
                    row_dict[key] = value['value']
                data.append(row_dict)

        except Exception as e:
            print(str(e))
            return []

        return data

    def parse_rdflib_results(self, results):
        """Parse result of sparql query (rdflib)

        Parameters
        ----------
        json_results : dict
            Query result

        Returns
        -------
        list
            Parsed results
        """
        variables = [str(v) for v in results.vars]
        data = []
        for row in results:
            row_dict = {}
            for v in variables:
                row_dict[v] = str(row[v])
            data.append(row_dict)

        return data

    def process_query(self, query):
        """Execute a query and return parsed results

        Parameters
        ----------
        query : string
            The query to execute

        Returns
        -------
        list
            Parsed results
        """
        # prefixed_query = self.get_sparl_prefix() + query
        logging.debug(query)
        if self.source_type == "sparql":
            return self.parse_sparql_results(self.execute_sparql_query(query))
        else:
            return self.parse_rdflib_results(self.execute_rdflib_query(query))
