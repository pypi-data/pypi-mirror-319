from collections.abc import Iterable
from collections import OrderedDict
from typing import Callable, Union
import pyfiglet 

class ForEachIterator:
    '''
    ForeachIterator: Utility class for iterables with enhanced functionality.
    Developed by: S Praveen
    -----------------------------------------------------------
    Use this class for advanced operations on any iterable.
    '''

    @staticmethod
    def print_docs():
        import pyfiglet
        print(pyfiglet.figlet_format("S Praveen"))
        print("ForeachIterator: A utility class for iterables.\nDeveloped by S Praveen")

    def __init__(self, data: Iterable) -> None:
        if not isinstance(data, Iterable):
            raise TypeError(f"Expected an iterable, got {type(data).__name__}")
        self.data = data

    @staticmethod
    def _validate_range(start: int, end: int, length: int):
        ''' 
        Helper method to validate the range of slicing indices.
        Ensures the start, end, and step values are within valid bounds.
        '''
        if start < 0 or end > length or start > end:
            raise ValueError(f"Invalid range: start={start}, end={end}, length={length}")

    @staticmethod
    def Foreach(data: Iterable, start: int = None, end: int = None, step: int = 1, 
                action: Callable[[Union[str, int]], None] = print) -> None:
        '''
        Iterate over the data and perform the specified action for each element.

        Args:
            data (Iterable): The input iterable to process.
            start (int): The start index for slicing (optional).
            end (int): The end index for slicing (optional).
            step (int): The step size for slicing (default is 1).
            action (Callable): A custom function to apply to each element (default is print).
        '''
        if not isinstance(data, Iterable):
            raise TypeError("Data must be an iterable.")
        
        data = list(data)  
        length = len(data)

        if start is not None and end is not None:
            ForEachIterator._validate_range(start, end, length)

        sliced_data = data[start:end:step] if start is not None and end is not None else data

        for item in sliced_data:
            action(item)

    @staticmethod
    def EnumForeach(data: Iterable, start: int = None, end: int = None, step: int = 1, 
                    enum_start: int = 1, action: Callable[[int, Union[str, int]], None] = print) -> None:
        '''
        Iterate over data and enumerate the items with their indices.

        Args:
            data (Iterable): The input iterable to process.
            start (int): The start index for slicing (optional).
            end (int): The end index for slicing (optional).
            step (int): The step size for slicing (default is 1).
            enum_start (int): The starting index for enumeration (default is 1).
            action (Callable): A custom function to apply to each (index, value) pair (default is print).
        '''
        if not isinstance(data, Iterable):
            raise TypeError("Data must be an iterable.")
        
        data = list(data)
        length = len(data)

        if start is not None and end is not None:
            ForEachIterator._validate_range(start, end, length)

        sliced_data = data[start:end:step] if start is not None and end is not None else data

        for idx, value in enumerate(sliced_data, start=enum_start):
            action(idx, value)

    @staticmethod
    def RemoveDuplicates(data: Iterable, start: int = None, end: int = None, step: int = 1) -> Iterable:
        '''
        Remove duplicates from the iterable while preserving the original order.

        Args:
            data (Iterable): The input iterable to process.
            start (int): The start index for slicing (optional).
            end (int): The end index for slicing (optional).
            step (int): The step size for slicing (default is 1).

        Returns:
            Iterable: A new iterable with duplicates removed, preserving the original order.
        '''
        if not isinstance(data, Iterable):
            raise TypeError("Data must be an iterable.")

        data = list(data)
        length = len(data)

        if start is not None and end is not None:
            ForEachIterator._validate_range(start, end, length)

        sliced_data = data[start:end:step] if start is not None and end is not None else data

        return list(OrderedDict.fromkeys(sliced_data))

    @staticmethod
    def GetDuplicates(data: Iterable, start: int = None, end: int = None, step: int = 1) -> Iterable:
        '''
        Get the duplicate elements from the iterable, preserving the order of first occurrence.

        Args:
            data (Iterable): The input iterable to process.
            start (int): The start index for slicing (optional).
            end (int): The end index for slicing (optional).
            step (int): The step size for slicing (default is 1).

        Returns:
            Iterable: A list of duplicate elements, preserving the order of first occurrence.
        '''
        if not isinstance(data, Iterable):
            raise TypeError("Data must be an iterable.")

        data = list(data)
        length = len(data)

        if start is not None and end is not None:
            ForEachIterator._validate_range(start, end, length)

        sliced_data = data[start:end:step] if start is not None and end is not None else data

        seen = set()
        duplicates = []

        for item in sliced_data:
            if item in seen:
                duplicates.append(item)
            else:
                seen.add(item)
        
        return duplicates

    @staticmethod
    def Filter(data: Iterable, filter_func: Callable[[Union[str, int]], bool]) -> Iterable:
        '''
        Filter the data based on a custom condition provided by the filter function.

        Args:
            data (Iterable): The input iterable to process.
            filter_func (Callable): A function that takes an element and returns True if it should be included.

        Returns:
            Iterable: A new iterable with elements that satisfy the filter condition.
        '''
        if not isinstance(data, Iterable):
            raise TypeError("Data must be an iterable.")
        
        return [item for item in data if filter_func(item)]

    @staticmethod
    def Transform(data: Iterable, transform_func: Callable[[Union[str, int]], Union[str, int]]) -> Iterable:
        '''
        Apply a transformation function to all elements in the iterable.

        Args:
            data (Iterable): The input iterable to process.
            transform_func (Callable): A function that takes an element and returns its transformed value.

        Returns:
            Iterable: A new iterable with transformed elements.
        '''
        if not isinstance(data, Iterable):
            raise TypeError("Data must be an iterable.")

        return [transform_func(item) for item in data]
    


if __name__=='__main__':

    ForEachIterator.Foreach('praveen', action=lambda x: print(x.upper())) 
    print()

    ForEachIterator.EnumForeach(tuple(range(10)), 3, 8, 2, action=lambda i, v: print(f"Index {i}, Value {v}"))
    print()

    print(ForEachIterator.RemoveDuplicates([1, 2, 3, 4, 5, 5, 6, 6, 6, 3, 1]))
    print()

    print(ForEachIterator.GetDuplicates([1, 2, 3, 4, 5, 5, 6, 6, 6, 3, 1]))
    print()

    print(ForEachIterator.Filter([1, 2, 3, 4, 5], filter_func=lambda x: x % 2 == 0))  
    print()

    print(ForEachIterator.Transform([1, 2, 3, 4], transform_func=lambda x: x ** 2))  
    print()

    print(ForEachIterator.__doc__)
    print()

    print(ForEachIterator.print_docs())