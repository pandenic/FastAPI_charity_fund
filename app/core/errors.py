from dataclasses import dataclass


@dataclass
class ErrorMessage:
    CHARITY_PROJECT_NAME_EXISTS = 'A charity project with that name already exists!'
    CHARITY_PROJECT_ID_NOT_FOUND = 'Charity project not found!'
    CHARITY_PROJECT_CANNOT_BE_DELETED = 'Charity project already fully invested and cannot be deleted!'
    CHARITY_PROJECT_FULL_AMOUNT_LT_INVESTED = 'Full amount should be greater than or equal to invested!'
