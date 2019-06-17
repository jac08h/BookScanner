from collections import OrderedDict

class Book:
    def __init__(self, od:OrderedDict):
        self.b = od

    def __get_authors(self) -> str:
        """
        Gets list of the authors.
        Returns:
            str
        """
        all_authors = self.b['authors']
        try:
            author = all_authors['author']['name'] # only one author

        except TypeError:  # Multiple authors
            for author in all_authors['author']:
                if author['role'] is None:  # not translator/ilustrator etc
                    author = author['name']

        return author


    def __str__(self):
        author = self.__get_authors()
        return f"""ISBN: {self.b['isbn']}
Title: {self.b['title']}
Author: {author}"""
