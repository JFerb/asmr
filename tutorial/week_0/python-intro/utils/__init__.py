from .example_module import average
from .tests import (
    test_list_indexing,
    test_slicing_1,
    test_slicing_2,
    test_create_array_with_zeros,
    test_fill_array_with_complement,
    test_set_odd_indices_to_zero,
    test_set_lower_right_value_to_one,
    test_bloodpressure_index,
    test_boolean_indexing,
    test_tvalue_computation,
    test_array_product_and_sum,
    test_compute_range_vectorized,
)

class Person:
    """ Example Person class. 
    
    Parameters
    ----------
    name : str
        Name of the person
    age : int/float
        Age of the person
    """
    def __init__(self, name, age):
        """ Initializes a Person object. """
        self.name = name
        self.age = age
        
    def introduce(self):
        """ Introduces the Person object. """
        print(f"Hi, I am {self.name}!")
        
    def is_older_than_30(self):
        """ Checks whether the person is older than 30. """
        older = self.age >= 30
        return older

    def increase_age(self, nr):
        """ Increases the age of the Person object by 'nr'.
        
        Parameters
        ----------
        nr : int
            Number to increase age with.
        """
        self.age = self.age + nr


__all__ = [
    "average",
    "Person",
    "test_list_indexing",
    "test_slicing_1",
    "test_slicing_2",
    "test_create_array_with_zeros",
    "test_fill_array_with_complement",
    "test_set_odd_indices_to_zero",
    "test_set_lower_right_value_to_one",
    "test_bloodpressure_index",
    "test_boolean_indexing",
    "test_tvalue_computation",
    "test_array_product_and_sum",
    "test_compute_range_vectorized",
]