def calculate_hike(current_ctc:int hike_percentage:int)->int:
hike_amount = (current_ctc * hike_percentage) // 100
new_ctc = current_ctc + hike_amount
return new_ctc

