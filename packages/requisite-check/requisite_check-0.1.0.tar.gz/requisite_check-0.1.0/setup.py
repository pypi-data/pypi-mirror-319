# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requisite_check']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'requisite-check',
    'version': '0.1.0',
    'description': 'Module for working with course requisite data and checking requisite satisfaciton.',
    'long_description': '# Requisite Processor\nThe `RequisiteProcessor` class is designed to evaluate whether the prerequisite rules for a course are met given a list of completed courses and test score data.\n\n## Prerequisite Data\nThis module can make use of any arbitrary prerequisite information given that it is formatted correctly. For more information on the necessary structure as well as the latest prerequsite data for UNM courses, see this repo:\n\nhttps://lobogit.unm.edu/unm-data-analytics/requisite-data#\n\n## Usage\n\n### Initialization\nInitialize the RequisiteProcessor with a dictionary of prerequisite rules.\n\n```python\nfrom requisite_processor import RequisiteProcessor\n\nprerequisite_rules = {\n    "202310": {\n        "MATH 1512": {\n            "type": "course",\n            "course": {"code": "MATH 1234"},\n            "minimum_course_grade": "C"\n        }\n    }\n}\n\nprocessor = RequisiteProcessor(prerequisite_rules)\n```\n\n### Processor Methods\nThe RequisiteProcessor contains the following methods:\n*availabile_academic_periods*:\nReturns a list of all academic periods in the dataset.\n```python\nacademic_periods = processor.availabile_academic_periods\nprint(academic_periods)  # Output: [\'202310\', \'202380\']\n```\n\n*latest_available_academic_period*:\nReturns the most recent academic period.\n```python\nlatest_period = processor.latest_available_academic_period\nprint(latest_period)  # Output: \'202380\'\n```\n\n*check_satisfaction*:\nChecks if a student satisfies the prerequisites for a course in a specific academic period.\n\nParameters:\n\n- course_code (str): Course to check prerequisites for.\n- courses_taken (list[dict], optional): List of completed courses and grades. Defaults to [].\n- test_scores (dict, optional): Test scores dictionary. Defaults to {}.\n- academic_period (str, optional): Academic period. Defaults to the latest available.\n- ignore_tests (bool, optional): Ignore test requirements. Defaults to False.\n- ignore_grades (bool, optional): Ignore grade requirements. Defaults to False.\n\nReturns:\nRequisiteCheckResult object. The result of the prerequisite check.\n\nSee below for example usage.\n\n### Example Prerequisite Satisfaction Check\n\n```python\ncourses_taken = [{"code": "MATH 1250", "grade": "B"}]\ntest_scores = {"A01": 28}\n\nresult = processor.check_satisfaction(\n    course_code="MATH 1512",\n    courses_taken=courses_taken,\n    test_scores=test_scores\n)\n\nprint(result.satisfied)  # Output: True or False\n```\n\n## Future Work\n- Write tests\n- Allow for more customization in how requisites are processed.\n- Write additional helper functions such as string representation of requirements, flattend requirements and more.',
    'author': 'Michael Hickman',
    'author_email': 'mhickman@unm.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
