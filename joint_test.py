import joint_locationHelperFunctions_test as jlh_t
import joint_collisionHelperFunctions_test as jch_t
def test_joint():
        p = True
        if not jlh_t.test_joint_locationComputation():
                p = False
        if not jch_t.test_joint_collisions():
                p = False
        return p

