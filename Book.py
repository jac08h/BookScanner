from collections import OrderedDict

class Book:
    def __init__(self, od:OrderedDict):
        self.b = od

    def __get_authors(self) -> list:
        """
        Gets list of the authors.
        Returns:
            list
        """
        all_authors = self.b['authors']
        try:
            author = all_authors['author']['name'] # only one author
            return list(author)

        except TypeError:  # Multiple authors
            authors = []
            for author in all_authors['author']:
                if author['role'] is None:  # not translator/ilustrator etc
                    authors.append(author['name'])

            return authors

    def __str__(self):
        authors = self.__get_authors()
        return f"""Title: {self.b['title']}
ISBN: {self.b['isbn']}j
Authors: {', '.join(authors)}"""

