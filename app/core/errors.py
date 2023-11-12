"""
Describe errors info.

class ErrorMessage: contains error messages for errors in the project
"""
from dataclasses import dataclass


@dataclass
class ErrorMessage:
    """Error messages text."""

    CHARITY_PROJECT_NAME_EXISTS = 'Проект с таким именем уже существует!'
    CHARITY_PROJECT_ID_NOT_FOUND = 'Charity project not found!'
    CHARITY_PROJECT_CANNOT_BE_DELETED = (
        'Charity project already fully invested and cannot be deleted!'
    )
    CHARITY_PROJECT_FULL_AMOUNT_LT_INVESTED = (
        'Full amount should be greater than or equal to invested!'
    )
    CHARITY_PROJECT_FULLY_INVESTED = 'Закрытый проект нельзя редактировать!'
    CHARITY_PROJECT_PARTLY_INVESTED = (
        'В проект были внесены средства, не подлежит удалению!'
    )
