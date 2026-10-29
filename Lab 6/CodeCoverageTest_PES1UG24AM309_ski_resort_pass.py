import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer

def test_code_coverage():
    # 1. Invalid input check (ValueError)
    with pytest.raises(ValueError):
        process_resort_bookings("invalid_groups", 10.0)

    # 2. Inactive group
    groups = [
        {"is_active": False},
        # Season pass, skier < 12, lodge locker
        {
            "is_active": True,
            "duration": "season",
            "includes_lodge_locker": True,
            "skiers": [{"age": 10, "gear_rental": True}]
        },
        # Half day, skier >= 65, invalid duration
        {
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 70, "gear_rental": False}]
        },
        # Invalid duration
        {
            "is_active": True,
            "duration": "invalid_duration"
        },
        # Full day (default duration), adult skier
        {
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 30}]
        },
        # Invalid skier age <= 0
        {
            "is_active": True,
            "skiers": [{"age": -1}]
        },
        # Blackout override with half day (break loop)
        {
            "is_active": True,
            "duration": "half_day",
            "skiers": [{"age": 25, "blackout_override": True}]
        },
        # Blackout override with non-half-day
        {
            "is_active": True,
            "duration": "full_day",
            "skiers": [{"age": 25, "blackout_override": True}]
        }
    ]
    res = process_resort_bookings(groups, 15.0)
    assert "total_revenue" in res

def test_audit_review_and_zero_sales():
    # Trigger AUDIT_REVIEW (rejected_passes > 4)
    groups = [{"is_active": True, "duration": "invalid"}] * 5
    res = process_resort_bookings(groups, 10.0)
    assert res["status"] == "AUDIT_REVIEW"

    # Trigger ZERO_SALES
    res_zero = process_resort_bookings([], 10.0)
    assert res_zero["status"] == "ZERO_SALES"

def test_check_chairlift_anemometer_coverage():
    # NO_DATA
    assert check_chairlift_anemometer([]) == "NO_DATA"
    # SUSPEND_LIFT
    assert check_chairlift_anemometer([[50, 50]]) == "SUSPEND_LIFT"
    # SAFE_OPERATION
    assert check_chairlift_anemometer([[30, 50, 30]]) == "SAFE_OPERATION"