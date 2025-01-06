import json
import sys
import json
import sys
import traceback
from typing import Any, Dict, List, Union, TypeVar
from .tools_eval import HasVal, DictKeyVal, DictKeyValMult, DictValCheck, AllHaveVal

T = TypeVar('T')

__all__ = [
    # Classes
    'AttrDict',
    
    # Dictionary conversion
    'AttrDictConv',
    'AttrDictUpd',
    
    # Dictionary operations
    'dict_of_dicts_sort',
    'DictContainsKeys',
    'DictKeyValIfElse',
    'DictKeyValFill',
    'DictKeyDel',
    'DictKeyVal',
    'DictKeyValMult',
    'DictValCheck'
]

class AttrDict(dict):
    """
    A dictionary subclass that allows attribute-style access to its items.
    Example:
        d = AttrDict({'foo': 'bar'})
        d.foo  # returns 'bar'
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = AttrDict(v)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'AttrDict' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            value = AttrDict(value)
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'AttrDict' object has no attribute '{name}'")

def AttrDictConv(d: Dict) -> AttrDict:
    """
    Convert a regular dictionary to AttrDict recursively.
    If no dict is provided, returns empty AttrDict.
    """
    if d is None:
        return AttrDict()
    return AttrDict(d)

def AttrDictUpd(d: Dict, updates: Dict) -> AttrDict:
    """
    Update an existing AttrDict with new keys from a dictionary.
    If no AttrDict is provided, creates a new one.
    """
    if d is None:
        d = {}
    if updates is None:
        updates = {}
    result = AttrDict(d)
    for k, v in updates.items():
        if isinstance(v, dict) and k in result and isinstance(result[k], dict):
            result[k] = AttrDictUpd(result[k], v)
        else:
            result[k] = v
    return result

def dict_of_dicts_sort(d: Dict[str, Dict], k: str, typ: str = 'float', rev: bool = False) -> Dict[str, Dict]:
    """
    Sort a dictionary of dictionaries by a specific key in the inner dictionaries.
    
    Args:
        d: Dictionary of dictionaries to sort
        k: Key in inner dictionaries to sort by
        typ: Type to convert values to ('float', 'str', 'int')
        rev: Whether to reverse sort order
    """
    sorted_d = {}
    vals_list = [str(d[pk][k]) for pk in d]
    sorted_vals_list = sorted(vals_list, reverse=rev)
    
    type_conv = {'float': float, 'str': str, 'int': int}
    conv = type_conv.get(typ, str)
    
    pks_list = []
    for val_tgt in sorted_vals_list:
        val_tgt = conv(val_tgt)
        for pk in d:
            if d[pk][k] == val_tgt:
                pks_list.append(pk)
    
    return {pk: d[pk] for pk in pks_list}

def DictKeyValIfElse(in_dict: Dict, k: str, d: Any) -> Any:
    """Return value if key is present and has value, else return default."""
    try:
        if k in in_dict and in_dict[k]:
            return in_dict[k]
        return d
    except Exception as e:
        print(f'DictKeyValIfElse ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

def DictKeyValFill(in_dict: Dict, k: str, v: Any) -> Any:
    """Build key if absent or fill with default value if empty."""
    try:
        if k not in in_dict or not in_dict[k]:
            in_dict[k] = v
        return in_dict[k]
    except Exception as e:
        print(f'DictKeyValFill ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

def DictKeyVal(in_dict: Dict, k: str) -> bool:
    """Check if key exists in dictionary."""
    try:
        return k in in_dict
    except Exception as e:
        print(f'DictKey ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

def DictKeyDel(in_dict: Dict, k: str) -> bool:
    """Delete key from dictionary if it exists."""
    try:
        if k in in_dict:
            del in_dict[k]
            return True
        return False
    except Exception as e:
        print(f'DictKeyDel ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

def DictKeyValMult(in_dict: Dict, ks: List[str]) -> bool:
    """Check if all keys exist and have non-None values."""
    return all(DictKeyVal(in_dict, k) for k in ks)

def DictContainsKeys(in_dict: Dict = {}, ks: Union[str, List[str]] = []) -> bool:
    """
    Check if all keys in ks are present in in_dict.
    ks can be either a single key or list of keys.
    """
    if isinstance(ks, str):
        ks = [ks]
    return set(ks).issubset(in_dict.keys())

def DictValCheck(in_dict: Dict = {}, ks: Union[str, List[str]] = [], show_yn: str = 'N') -> bool:
    """
    Verify all specified values in dict have value.
    ks - allows specified keys to be checked
    show_yn - if 'Y', prints keys with no value
    """
    if not HasVal(ks):
        return True
        
    if isinstance(ks, str):
        ks = [ks]
        
    for k in ks:
        if k not in in_dict:
            return False
        v = in_dict[k]
        if not HasVal(v):
            if show_yn == 'Y':
                print(f'{k} : {v}')
            return False
    return True

def dict_upd(d, e, k, v):
    if not e in d: d[e] = {}
    d[e][k] = v
    return d

def print_dict(d):
    print('')
    print('')
    print(json.dumps(d, indent=4))
    print(d)
    print('')
    print('')
    return

