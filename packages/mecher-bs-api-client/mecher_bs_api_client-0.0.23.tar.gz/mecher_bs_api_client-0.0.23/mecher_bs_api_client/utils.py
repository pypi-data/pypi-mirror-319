from typing import Union, Iterable, List, Callable, Any

from easydict import EasyDict


def compound_list_to_easydict(array: Union[object, Iterable]) -> Union[EasyDict, List, object]:
    if isinstance(array, list):
        return list(map(compound_list_to_easydict, array))
    elif isinstance(array, dict):
        return EasyDict(array)
    else:
        return array


def get_element_from_list(list_for_search: list,
                          function_for_search: Callable,
                          error_hint: str = 'Error during searching element in list',
                          not_found_ok: bool = False,
                          allow_duplicates: bool = False) -> Any:
    """
    In case of allow_duplicates = True and multiple results return the first element
    """
    if not list_for_search:
        return

    element = None
    filtered_list = list(filter(function_for_search, list_for_search))
    match len(filtered_list):
        case 0:
            if not not_found_ok:
                raise Exception(f'{error_hint} - Not found')
        case 1:
            element = filtered_list[0]
        case _:
            if not allow_duplicates:
                raise Exception(
                    f'{error_hint} - There are multiple elements (founded {len(filtered_list)} elements)')
            element = filtered_list[0]

    return element
