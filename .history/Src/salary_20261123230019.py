def calculate_hike(current_ctc;int hike_percentage:int)->int:
    """
    Calculate the new CTC after applying the hike percentage.

    Parameters:
    current_ctc (int): The current CTC of the employee.
    hike_percentage (int): The percentage hike to be applied.

    Returns:
    int: The new CTC after applying the hike.
    """
    new_ctc = current_ctc + (current_ctc * hike_percentage / 100)
    return int(new_ctc)