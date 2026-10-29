import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer

def test_value_error_branches():
    # Test non-list groups branch
    with pytest.raises(ValueError):
        process_resort_bookings("not_a_list", 10.0)
    # Test negative facility_fee branch
    with pytest.raises(ValueError):
        process_resort_bookings([], -5.0)

def test_booking_branches_comprehensive():
    groups = [
        # Inactive group branch
        {"is_active": False},
        
        # Season pass + age < 12 branch + gear_rental True + includes_lodge_locker True
        {
            "is_active": True,
            "duration": "season",
            "includes_lodge_locker": True,
            "skiers": [{"age": 10, "gear_rental": True}]
        },
        
        # Full day + age >= 65 branch + gear_rental False + includes_lodge_locker False
        {
            "is_active": True,
            "duration": "full_day",
            "includes_lodge_locker": False,
            "skiers": [{"age": 70, "gear_rental": False}]
        },
        
        # Half day + regular age (between 12 and 64) branch
        {
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 30, "gear_rental": False}]
        },
        
        # Invalid pass duration (else branch)
        {
            "is_active": True,
            "duration": "unknown_pass",
            "skiers": [{"age": 25}]
        },
        
        # Invalid age <= 0 branch
        {
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 0}]
        },
        
        # Blackout override True AND duration == "half_day" (group_total=0.0 & break)
        {
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 25, "blackout_override": True}]
        },
        
        # Blackout override True AND duration != "half_day"
        {
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 25, "blackout_override": True}]
        }
    ]
    res = process_resort_bookings(groups, 20.0)
    assert res["status"] == "COMPLETED"

def test_audit_review_branch():
    # Force rejected_passes > 4 branch
    invalid_groups = [{"is_active": True, "duration": "bad_type"}] * 5
    res = process_resort_bookings(invalid_groups, 10.0)
    assert res["status"] == "AUDIT_REVIEW"

def test_zero_sales_branch():
    # Force total_revenue == 0.0 branch
    res = process_resort_bookings([], 10.0)
    assert res["status"] == "ZERO_SALES"

def test_anemometer_branches():
    # wind_streams empty branch
    assert check_chairlift_anemometer([]) == "NO_DATA"
    
    # speed_mph > 45 True branch -> streak >= 2 -> SUSPEND_LIFT
    assert check_chairlift_anemometer([[50, 50]]) == "SUSPEND_LIFT"
    
    # speed_mph > 45 False branch (reset streak) -> SAFE_OPERATION
    assert check_chairlift_anemometer([[50, 20, 50]]) == "SAFE_OPERATION"