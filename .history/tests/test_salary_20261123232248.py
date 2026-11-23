from Src.salary import calculate_hike

def test_hike():
    # 15 LPA pe 30% hike = 19 LPA hona chahiye
    result = calculate_hike(15, 30)
    assert result == 19
    print("Test Pass Ho Gaya - Hike Sahi Hai!")

test_hike()