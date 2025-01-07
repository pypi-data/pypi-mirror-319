from __future__ import annotations

import copyreg
from io import BytesIO
from pickle import PicklingError
from typing import Any, Callable

import dill

loads = dill.loads


class CouldNotBePickled:
    def __init__(self, class_name: str) -> None:
        self.class_name = class_name

    def __repr__(self) -> str:
        return f"Item of type '{self.class_name}' could not be pickled and was omitted."

    @classmethod
    def reduce(cls, item: Any) -> tuple[Callable[[str], CouldNotBePickled], tuple[str]]:
        return cls, (type(item).__name__,)


class Pickler(dill.Pickler):
    """ Overload dill to ignore unpicklable parts of objects.
        You probably didn't want to use these parts anyhow.
        However, if you did, you'll have to find some way to make them picklable.
    """
    def save(self, obj: Any, save_persistent_id: bool = True) -> None:
        """ Copied from pickle and amended. """
        self.framer.commit_frame()

        # Check for persistent id (defined by a subclass)
        pid = self.persistent_id(obj)
        if pid is not None and save_persistent_id:
            self.save_pers(pid)
            return

        # Check the memo
        x = self.memo.get(id(obj))
        if x is not None:
            self.write(self.get(x[0]))
            return

        rv = NotImplemented
        reduce = getattr(self, "reducer_override", None)
        if reduce is not None:
            rv = reduce(obj)

        if rv is NotImplemented:
            # Check the type dispatch table
            t = type(obj)
            f = self.dispatch.get(t)
            if f is not None:
                f(self, obj)  # Call unbound method with explicit self
                return

            # Check private dispatch table if any, or else
            # copyreg.dispatch_table
            reduce = getattr(self, 'dispatch_table', copyreg.dispatch_table).get(t)
            if reduce is not None:
                rv = reduce(obj)
            else:
                # Check for a class with a custom metaclass; treat as regular
                # class
                if issubclass(t, type):
                    self.save_global(obj)
                    return

                # Check for a __reduce_ex__ method, fall back to __reduce__
                reduce = getattr(obj, "__reduce_ex__", None)
                try:
                    if reduce is not None:
                        rv = reduce(self.proto)
                    else:
                        reduce = getattr(obj, "__reduce__", None)
                        if reduce is not None:
                            rv = reduce()
                        else:
                            raise PicklingError("Can't pickle %r object: %r" %
                                                (t.__name__, obj))
                except Exception:  # noqa
                    rv = CouldNotBePickled.reduce(obj)

        # Check for string returned by reduce(), meaning "save as global"
        if isinstance(rv, str):
            try:
                self.save_global(obj, rv)
            except Exception:  # noqa
                self.save_global(obj, CouldNotBePickled.reduce(obj))
            return

        # Assert that reduce() returned a tuple
        if not isinstance(rv, tuple):
            raise PicklingError("%s must return string or tuple" % reduce)

        # Assert that it returned an appropriately sized tuple
        length = len(rv)
        if not (2 <= length <= 6):
            raise PicklingError("Tuple returned by %s must have "
                                "two to six elements" % reduce)

        # Save the reduce() output and finally memoize the object
        try:
            self.save_reduce(obj=obj, *rv)
        except Exception:  # noqa
            self.save_reduce(obj=obj, *CouldNotBePickled.reduce(obj))


def dumps(obj: Any, protocol: str = None, byref: bool = None, fmode: str = None, recurse: bool = True,
          **kwds: Any) -> bytes:
    """pickle an object to a string"""
    protocol = dill.settings['protocol'] if protocol is None else int(protocol)
    _kwds = kwds.copy()
    _kwds.update(dict(byref=byref, fmode=fmode, recurse=recurse))
    with BytesIO() as file:
        Pickler(file, protocol, **_kwds).dump(obj)
        return file.getvalue()
