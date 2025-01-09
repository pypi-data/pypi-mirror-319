from src.angle_tompy.angle import Angle, combine_angles


# def test_angle_combine_angles_success():
#     # Setup
#     angle0: Angle = Angle(degree=0)
#     angle1: Angle = Angle(degree=1)
#     angles0: list[frozenset[Angle]] = [frozenset([angle0]), frozenset([angle1])]
#     combined_angles0: set[tuple[Angle, ...]] = {(angle0, angle1)}
#
#     # Execution
#     combined_angles1: set[tuple[Angle, ...]] = combine_angles(angles=angles0)
#
#     # Validation
#     assert combined_angles0 == combined_angles1
