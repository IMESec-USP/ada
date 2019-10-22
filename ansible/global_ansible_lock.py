import threading
import os
from .lock_exception import AnsibleLockException

LOCK_TIMEOUT_IN_SECONDS = 3

class __GlobalLock:

    def __init__(self):
        self.__lock = threading.Lock()
        self.__thread_that_locked = None

    def __enter__(self):
        lock_result = self.__lock.acquire(timeout=LOCK_TIMEOUT_IN_SECONDS)
        if not lock_result:
            raise AnsibleLockException('could not lock GlobalLock')

        print(f'setting thread that locked to {threading.get_ident()}')
        self.__thread_that_locked = threading.get_ident()
        
        return lock_result

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.__thread_that_locked == threading.get_ident():
            self.__lock.release()

# I hate singletons, but __enter__ and __exit__
# don't work when GlobalLock is a static class
GlobalLock = __GlobalLock()

if __name__ == '__main__':
    # Tests
    import time
    def competing_lock():
        time.sleep(1)
        try:
            with GlobalLock:
                pass
        except AnsibleLockException as e:
            print(f'Caught AnsibleLockException inside thread: {e}')

    thread = threading.Thread(target=competing_lock, args=tuple())
    thread.start()
    with GlobalLock as res:
        print(res)
        time.sleep(4)