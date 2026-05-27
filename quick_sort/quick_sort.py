def quick_sort(array):
    # Base case: if the list is empty or has one element, it's already sorted
    if len(array) <= 1:
        return array
    
    # create the pivot value
    p_first = array[0]

    p1_sublist = [x for x in array if x < p_first]
    p2_sublist = [x for x in array if x == p_first]
    p3_sublist = [x for x in array if x > p_first]

    # recursively sort the sublists
    sorted_p1 = quick_sort(p1_sublist)
    sorted_p3 = quick_sort(p3_sublist)

    # combine the sorted sublists
    return sorted_p1 + p2_sublist + sorted_p3