from my_robot_nav.base import in_deadzone


def test_inside_deadzone_is_true():
    assert in_deadzone(0.0, 0.0, 0.005, 0.01) is True


def test_linear_outside_tolerance_is_false():
    assert in_deadzone(0.5, 0.0, 0.0, 0.0) is False


def test_angular_outside_tolerance_is_false():
    assert in_deadzone(0.0, 0.5, 0.0, 0.0) is False


def test_boundary_is_not_in_deadzone():
    # tolerance is strict (<), so exactly-at-tol is NOT in the deadzone
    assert in_deadzone(0.02, 0.0, 0.0, 0.0, linear_tol=0.02) is False


def test_custom_tolerances_respected():
    assert in_deadzone(0.1, 0.0, 0.0, 0.0, linear_tol=0.2) is True
