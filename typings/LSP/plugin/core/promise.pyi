from _typeshed import Incomplete
from typing import Callable, Generic, Protocol, TypeVar

T = TypeVar('T')
S = TypeVar('S')
TExecutor = TypeVar('TExecutor')
T_contra = TypeVar('T_contra', contravariant=True)
TResult = TypeVar('TResult')

class ResolveFunc(Protocol[T_contra]):
    def __call__(self, resolve_value: T_contra) -> None: ...

FullfillFunc: Incomplete
ExecutorFunc = Callable[[ResolveFunc[T]], None]
PackagedTask: Incomplete

class Promise(Generic[T]):
    '''A simple implementation of the Promise specification.

    See: https://promisesaplus.com

    Promise is in essence a syntactic sugar for callbacks. Simplifies passing
    values from functions that might do work in asynchronous manner.

    Example usage:

      * Passing return value of one function to another:

        def do_work_async(resolve):
            # "resolve" is a function that, when called with a value, resolves
            # the promise with provided value and passes the value to the next
            # chained promise.
            resolve(111)  # Can be invoked asynchronously.

        def process_value(value):
            assert value === 111

        Promise(do_work_async).then(process_value)

      * Returning Promise from chained promise:

        def do_work_async_1(resolve):
            # Compute value asynchronously.
            resolve(111)

        def do_work_async_2(resolve):
            # Compute value asynchronously.
            resolve(222)

        def do_more_work_async(value):
            # Do more work with the value asynchronously. For the sake of this
            # example, we don\'t use \'value\' for anything.
            assert value === 111
            return Promise(do_work_async_2)

        def process_value(value):
            assert value === 222

        Promise(do_work_async_1).then(do_more_work_async).then(process_value)
    '''
    @staticmethod
    def resolve(resolve_value: S) -> Promise[S]:
        """Immediately resolves a Promise.

        Convenience function for creating a Promise that gets immediately
        resolved with the specified value.

        Arguments:
            resolve_value: The value to resolve the promise with.
        """
    resolver: ResolveFunc[TExecutor] | None
    @staticmethod
    def packaged_task() -> PackagedTask[S]: ...
    @staticmethod
    def all(promises: list[Promise[S]]) -> Promise[list[S]]:
        """
        Takes a list of promises and returns a Promise that gets resolved when all promises
        gets resolved.

        :param      promises: The list of promises

        :returns:   A promise that gets resolved when all passed promises gets resolved.
                    Gets passed a list with all resolved values.
        """
    resolved: bool
    mutex: Incomplete
    callbacks: list[ResolveFunc[T]]
    def __init__(self, executor_func: ExecutorFunc[T]) -> None:
        '''Initialize Promise object.

        Arguments:
            executor_func: A function that is executed immediately by this Promise.
            It gets passed a "resolve" function. The "resolve" function, when
            called, resolves the Promise with the value passed to it.
        '''
    def __repr__(self) -> str: ...
    def then(self, onfullfilled: FullfillFunc[T, TResult]) -> Promise[TResult]:
        """Create a new promise and chain it with this promise.

        When this promise gets resolved, the callback will be called with the
        value that this promise resolved with.

        Returns a new promise that can be used to do further chaining.

        Arguments:
            onfullfilled: The callback to call when this promise gets resolved.
        """
    value: Incomplete
    def _do_resolve(self, new_value: T) -> None: ...
    def _add_callback(self, callback: ResolveFunc[T]) -> None: ...
    def _is_resolved(self) -> bool: ...
    def _get_value(self) -> T: ...
