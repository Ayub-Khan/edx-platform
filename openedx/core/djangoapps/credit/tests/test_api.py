""" Module contains the tests for api """

from opaque_keys.edx.keys import CourseKey
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from openedx.core.djangoapps.credit.exceptions import InvalidCreditRequirements
from openedx.core.djangoapps.credit.models import CreditCourse
from openedx.core.djangoapps.credit.api import set_credit_requirements, get_credit_requirements


class ApiTestCases(ModuleStoreTestCase):
    """ Test for models """

    def setUp(self, **kwargs):
        super(ApiTestCases, self).setUp()
        self.course_key = CourseKey.from_string("edX/DemoX/Demo_Course")

    def test_set_credit_requirements_invalid_credit_course(self):
        with self.assertRaises(InvalidCreditRequirements):
            requirements = [
                {
                    "namespace": "grade",
                    "name": "grade",
                    "configuration": {
                        "min_grade": 0.8
                    }
                }
            ]
            set_credit_requirements(self.course_key, requirements)

    def test_set_credit_requirements_invalid_requirements(self):
        self.add_credit_course()
        requirements = [
            {
                "namespace": "grade",
                "configuration": {
                    "min_grade": 0.8
                }
            }
        ]
        with self.assertRaises(InvalidCreditRequirements):
            set_credit_requirements(self.course_key, requirements)

    def test_set_credit_requirements(self):
        self.add_credit_course()
        requirements = [
            {
                "namespace": "grade",
                "name": "grade",
                "configuration": {
                    "min_grade": 0.8
                }
            },
            {
                "namespace": "grade",
                "name": "grade",
                "configuration": {
                    "min_grade": 0.8
                }
            }
        ]
        self.assertIsNone(set_credit_requirements(self.course_key, requirements))

    def test_get_credit_requirements(self):
        self.add_credit_course()
        requirements = [
            {
                "namespace": "grade",
                "name": "grade",
                "configuration": {
                    "min_grade": 0.8
                }
            },
            {
                "namespace": "grade",
                "name": "grade",
                "configuration": {
                    "min_grade": 0.8
                }
            }
        ]
        set_credit_requirements(self.course_key, requirements)
        self.assertEquals(len(get_credit_requirements(self.course_key)), 1)

    def add_credit_course(self):
        """ Mark the course as a credit """

        credit_course = CreditCourse(course_key=self.course_key, enabled=True)
        credit_course.save()
        return credit_course