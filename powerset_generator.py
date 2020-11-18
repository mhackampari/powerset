import logging
import sys

from powerset import format_output
from powerset import parse_input
from powerset import powerset_pythonic

logger = logging.getLogger('Powerset')
logger.setLevel(logging.ERROR)
ch = logging.FileHandler('powerset_error.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    try:
        elements = parse_input(sys.argv[1])
    except IndexError:
        logger.error('No argument was provided. Exit.')
        sys.exit(
            """Input argument is missing. Please provide a string complaint to the following regular expression: '\w+(\,\w+)*'""")
    except ValueError:
        logger.error('The passed input does not respect the following regular expression: \w+(\,\w+)*')
        sys.exit('Your input does not respect this regular expression: \w+(\,\w+)*')

    try:
        iter_powerset = powerset_pythonic(elements)
        print(*format_output(iter_powerset), sep='\n')
    except MemoryError as e:
        exception_name = e.__class__.__name__
        logger.error('The program has exited due to {} exception'.format(exception_name))
        sys.exit(
            '{}: It is an O(n*2^n) algorithm in memory and space. Watch out for the input length. Try with less input elements.'.format(
                str(exception_name)))


if __name__ == "__main__":
    main()
