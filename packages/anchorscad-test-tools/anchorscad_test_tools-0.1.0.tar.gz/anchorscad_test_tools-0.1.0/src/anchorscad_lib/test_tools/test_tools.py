'''
Created on 14 Jan 2021

@author: gianni

iterable_assert is a test heler that provides more information about the
difference between two iterables based an expecation function. It also provides
more information about the location of the difference.
'''

from dataclasses import dataclass

@dataclass
class _AssertionException(Exception):
    depth: tuple
    msg: str=None
    ex: Exception = None
    
    def explain(self):
        if self.msg:
            return self.msg
        if self.ex:
            return str(self.ex)
        return 'No explanation'
    
class IterableAssert(Exception):
    '''Exception in iterable_assert'''
    
    
def is_iterable(v):
    """Return True if v is an iterable."""
    if isinstance(v, str):
        return False
    try:
        # isinstance(v, Iterable) is not true for duck types.
        # resorting to actually calling iter().
        iter(v) 
        return True
    except TypeError:
        return False

def _iterable_assert(expect_fun, va, vb, *args, depth=(), **kwargs):
    ii_va = is_iterable(va)
    ii_vb = is_iterable(vb)

    both_true = ii_va and ii_vb
    
    if both_true:
        try:
            assert len(va) == len(vb), (
                f'Lengths different depth={depth} len(va)={len(va)} != len(vb)={len(vb)}')
            for i, evab in enumerate(zip(va, vb)):
                eva, evb = evab
                _iterable_assert(expect_fun, eva, evb, *args, depth=depth + (i,), **kwargs)
        except _AssertionException:
            raise
        except BaseException as ex:
            raise _AssertionException(depth, ex=ex)
    elif not (ii_va or ii_vb):
        try:
            assert not ii_va and not ii_vb
            expect_fun(va, vb, *args, **kwargs)
        except _AssertionException:
            raise
        except (BaseException, AssertionError) as ex:
            raise _AssertionException(depth, ex=ex)
    else:
        exp = 'va is iterable and vb is not' if ii_vb else 'vb is iterable and va is not'
        raise _AssertionException(depth, msg=exp)

def iterable_assert(expect_fun, va, vb, *args, **kwargs):
    """
    Assert that two iterables match the expected function.

    Args:
        expect_fun: The function to use to compare the iterables.
        va: The first iterable value
        vb: The second iterable value
        *args: Additional arguments to pass to the expected function.
        **kwargs: Additional keyword arguments to pass to expect_fun.

    Raises:
        IterableAssert: Exception raised if the iterables do not match the expected function.
    """
    try:
        _iterable_assert(expect_fun, va, vb, *args, **kwargs)
    except _AssertionException as e:
        msg = f'depth={e.depth!r}\nva={va!r}\nvb={vb!r}\n'
        raise IterableAssert(f"{msg}\n{str(e.explain())}")

