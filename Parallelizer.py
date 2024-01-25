import concurrent.futures
import os
from functools import wraps


# def make_parallel(func):
#     """
#         Decorator used to decorate any function which needs to be parallized.
#         After the input of the function should be a list in which each element is a instance of input fot the normal function.
#         You can also pass in keyword arguements seperatley.
#         :param func: function
#             The instance of the function that needs to be parallelized.
#         :return: function
#     """

#     @wraps(func)
#     def wrapper(lst, return_type='list', *args, **kwargs):
#         """
#         :param lst:
#             The inputs of the function in a list.
#         :return:
#         """
#         # the number of threads that can be max-spawned.
#         # If the number of threads are too high, then the overhead of creating the threads will be significant.
#         # Here we are choosing the number of CPUs available in the system and then multiplying it with a constant.
#         # In my system, i have a total of 8 CPUs so i will be generating a maximum of 16 threads in my system.
#         # You can change this multiple according to you requirement
#         number_of_threads_multiple = 2
#         number_of_workers = int(os.cpu_count() * number_of_threads_multiple)
#         if len(lst) < number_of_workers:
#             # If the length of the list is low, we would only require those many number of threads.
#             # Here we are avoiding creating unnecessary threads
#             number_of_workers = len(lst)

#         if number_of_workers:
#             if number_of_workers == 1:
#                 # If the length of the list that needs to be parallelized is 1, there is no point in
#                 # parallelizing the function.
#                 # So we run it serially.
#                 result = [func(lst[0], **kwargs)]
#             else:
#                 # Core Code, where we are creating max number of threads and running the decorated function in parallel.
#                 if return_type == 'list':
#                     result = []
#                     with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:
#                         bag = {executer.submit(
#                             func, i, **kwargs): i for i in lst}
#                         for future in concurrent.futures.as_completed(bag):
#                             result.append(future.result())
#                 elif return_type == 'dict':
#                     result = {}
#                     with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:
#                         bag = {executer.submit(
#                             func, i, **kwargs): i for i in lst}
#                         for future in concurrent.futures.as_completed(bag):
#                             result[bag[future]] = future.result()
#                 else:
#                     result = []
#         else:
#             result = []
#         return result
#     return wrapper

def make_parallel(func):
    """
        Decorator used to decorate any function which needs to be parallized.
        After the input of the function should be a list in which each element is a instance of input fot the normal function.
        You can also pass in keyword arguements seperatley.
        :param func: function
            The instance of the function that needs to be parallelized.
        :return: function

        Example usage:
        @make_parallel
        def func(i: int):
            print(i)
        func([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    """

    @wraps(func)
    def wrapper(lst, *args, **kwargs):
        """
        :param lst:
            The inputs of the function in a list.
        :return:
        """
        # number_of_workers = int(os.cpu_count() * 2)
        number_of_workers = 4
        # if len(lst) < number_of_workers:
        #     number_of_workers = len(lst)

        result = []
        if number_of_workers:
            if number_of_workers == 1:
                result = [func(lst[0], *args, **kwargs)]
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_workers) as executer:
                    bag = {executer.submit(
                        func,  i, *args, **kwargs): i for i in lst}
                    for future in bag:
                        result.append(future.result())

        # remove None value
        result = [i for i in result if i]
        return result
    return wrapper
