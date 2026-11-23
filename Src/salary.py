def calculate_hike(current_ctc: int, hike_percent: int) -> int:
    hike_amount = current_ctc * hike_percent // 100
    new_ctc = current_ctc + hike_amount
    return new_ctc

def calculate_monthly_salary(yearly_ctc_lpa: int) -> int:
    return yearly_ctc_lpa * 100000 // 12