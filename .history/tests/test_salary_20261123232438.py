import sys
import os

# Python ko bataya - src folder kaha hai
# Jaise C# me tum Project Reference dete the, waisa hi hai
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from salary import calculate_hike

def test_hike():
    # 15 LPA pe 30% hike = 19 LPA hona chahiye
    result = calculate_hike(15, 30)
    assert result == 19
    print("Test Pass Ho Gaya - Hike Sahi Hai!")

test_hike()