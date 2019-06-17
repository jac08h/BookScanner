import json
import logging
import requests
import xmltodict
from collections import OrderedDict
from xml.parsers.expat import ExpatError
import argparse

from Book import Book
from exceptions import *

def get_key_and_secret(secrets_file:str='secrets.json')->tuple:
    """
    Read key and secret from json file.

    Args:
        secrets_file
    Raises:
        ReadingSecretsError: An error occurred reading secrets file
    Returns:
        Tuple containing api key and secret
    """
    with open(secrets_file) as fp:
        try:
            data = json.load(fp)
        except json.decoder.JSONDecodeError:
            logging.error(f"Error reading secrets file ({secrets_file})")
            raise ReadingSecretsError
    try:
        key = data["key"]
        secret = data["secret"]
        return key, secret

    except KeyError:
        logging.error(f"Missing key or secret ({secrets_file})")
        raise ReadingSecretsError

def get_book_data(isbn:str, api_key:str) -> OrderedDict:
    """
    Gets book data using Goodreads API

    Args:
        isbn
        api_key: goodreads api key
    Raises::
        WrongISBNError::
    Returns:
        Ordered dict of book data

    """
    try:
        int_isbn = int(isbn)
    except ValueError:
        logging.error(f"Invalid ISBN format ({isbn})")
        raise WrongISBNError

    if int_isbn <= 0:
        logging.error(f"ISBN has to be greater than zero({isbn})")
        raise WrongISBNError

    url = f"https://www.goodreads.com/book/isbn/{isbn}?key={api_key}"

    r = requests.get(url)
    try:
        data = xmltodict.parse(r.text)
    except ExpatError:
        logging.error(f"Invalid key")
        raise InvalidKey

    try:
        book_data = data["GoodreadsResponse"]["book"]
        return book_data
    except KeyError:
        logging.error(f"Book not found({isbn})")
        raise WrongISBNError



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("isbn")
    args = parser.parse_args()

    isbn = args.isbn
    key, secret = get_key_and_secret()
    b_data = get_book_data(isbn, key)
    b = Book(b_data)
    print(b)