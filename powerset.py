import logging
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
ch = logging.StreamHandler()
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


def powerset_dfs(iterable: List[Any]) -> List[List[Any]]:
    """
    Depth first traversal method to solve the powerset problem

    :param iterable: List of elements from which to generate the powerset
    :return: Iterable result
    """
    result = list()
    for index, elem in enumerate(iterable):
        _recur_dfs([elem], iterable[index + 1:], result)

    return result


def _recur_dfs(prevres: List[Any], iterable: List[Any], result: List[List[Any]]):
    result.append(prevres[:])

    for index, elem in enumerate(iterable):
        curr_res = prevres[:]
        curr_res.append(elem)
        _recur_dfs(curr_res, iterable[index + 1:], result)


def _concat(curr, elem):
    return curr + [elem]


def powerset_mp(iterable: Iterable) -> List[List[Any]]:
    pool = Pool(processes=None)
    output = [[]]

    for elem in iterable:
        output += pool.starmap(_concat, zip(output, repeat(elem)))

    return output[1:]


def powerset_iterative(iterable: Iterable) -> List[List[Any]]:
    output = [[]]

    for elem in iterable:
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
        sys.exit(
            'Input argument is missing. Please provide a string complaint to the following regular expression: "[0-9a-zA-Z]+(\,[0-9a-zA-Z]+)+"')

    iter_powerset = powerset_dfs(elements)
    print(format_output(iter_powerset))


if __name__ == "__main__":
    main()
