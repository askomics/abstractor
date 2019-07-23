from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlQuery():
    """SPARQL methods"""

    def __init__(self, endpoint, prefix, prefixes):
        """Init

        Parameters
        ----------
        endpoint : string
            SPARQL endpoint url
        prefix : string
            Prefix URI :
        prefixes : dict
            Common prefixes
        """
        self.endpoint = endpoint
        self.prefix = prefix
        self.prefixes = prefixes

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

    def execute_query(self, query):
        """Execute a sparql query

        Parameters
        ----------
        query : string
            Query to perform

        Returns
        -------
        TYPE
            result
        """
        endpoint = SPARQLWrapper(self.endpoint)
        prefixed_query = self.get_sparl_prefix() + query
        # print(prefixed_query)
        endpoint.setQuery(prefixed_query)

        endpoint.setReturnFormat(JSON)
        try:
            results = endpoint.query().convert()
        except Exception as e:
            raise e

        return results

    def parse_results(self, json_results):
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
        return self.parse_results(self.execute_query(query))

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
        return uri.split("/")[-1].split("#")[-1]
