import logging
import re
import sys
from itertools import chain
from itertools import combinations
from itertools import repeat
from multiprocessing import Pool
from typing import Any
from typing import Iterable
from typing import List
from typing import Tuple

logger = logging.getLogger('Powerset')
logger.setLevel(logging.ERROR)
ch = logging.FileHandler('powerset_error.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def powerset_pythonic(iterable: Iterable) -> Iterable[Tuple[Any]]:
    """
    Lazily generation of the powerset

    :param iterable: Iterable of elements
    :return: Iterable of elements
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def powerset_dfs(inlist: List[Any]) -> List[List[Any]]:
    """
    Depth first traversal method to solve the powerset problem

    :param inlist: List of elements from which to generate the powerset
    :return: Iterable result
    """
    result = list()
    for index, elem in enumerate(inlist):
        _recur_dfs([elem], inlist[index + 1:], result)

    return result


def _recur_dfs(prevres: List[Any], iterable: List[Any], result: List[List[Any]]):
    """Private recursive auxiliary method with depth first traversal which is used for powerset generation"""
    result.append(prevres[:])

    for index, elem in enumerate(iterable):
        curr_res = prevres[:]
        curr_res.append(elem)
        _recur_dfs(curr_res, iterable[index + 1:], result)


def _concat(curr, elem):
    """Private auxiliary method for multiprocessing powerset computation"""
    return curr + [elem]


def powerset_mp(inlist: List[Any]) -> List[List[Any]]:
    """
    Multiprocessing version of powerset algorithm.

    :param inlist: List of elements from which to generate the powerset.
    :return: Powerset list.
    """
    pool = Pool(processes=None)
    output = [[]]

    for elem in inlist:
        output += pool.starmap(_concat, zip(output, repeat(elem)))

    return output[1:]


def powerset_iterative(inlist: List[Any]) -> List[List[Any]]:
    """
    Iterative version of powerset algorithm.

    :param inlist: List of elements from which to generate the powerset.
    :return: Powerset list.
    """
    output = [[]]

    for elem in inlist:
        tmp = []
        for curr in output:
            tmp.append(curr + [elem])
        output += tmp

    return output[1:]


def parse_input(raw_input: str) -> List[str]:
    """
    Parses command line string transforming it into a list of strings.

    :param raw_input: string to parse which respects this pattern str(,str)*
    :return: list of strings
    """
    if not re.match('\w+(,\w+)*', raw_input, re.LOCALE):
        raise ValueError
    return raw_input.split(',')


def format_output(powerset: Iterable) -> str:
    """
    Format intermediate result to expected multiline string

    :param powerset: Iterable powerset
    :return: Formatted multiline output
    """
    return '\n'.join(map(lambda elem_set: ','.join(elem_set), powerset))


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

    iter_powerset = powerset_pythonic(elements)
    print(format_output(iter_powerset))


if __name__ == "__main__":
    main()
