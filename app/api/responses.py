from fastapi import status


UNAUTHORIZED_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string'}
    },
    'required': ['detail']
}
FORBIDDEN_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string'}
    },
    'required': ['detail']
}
UNAUTHORIZED_RESPONSE = {
    'description': 'Unauthorized',
    'content': {
        'application/json': {
            'schema': UNAUTHORIZED_SCHEMA
        }
    }
}
FORBIDDEN_RESPONSE = {
    'description': 'Not a superuser.',
    'content': {
        'application/json': {
            'schema': FORBIDDEN_SCHEMA
        }
    }
}
NOT_FOUND_RESPONSE = {
    'description': 'The project does not exist',
    'content': {
        'application/json': {
            'schema': {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    }
}
CHARITY_PROJECT_CREATE_EXTRA_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Not unique name',
        'content': {
            'application/json': {
                'examples': {
                    'notUniqueName': {
                        'value': {
                            'detail': 'Проект с таким именем уже существует!'
                        }
                    }
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE,
    status.HTTP_403_FORBIDDEN: FORBIDDEN_RESPONSE
}
CHARITY_PROJECT_UPDATE_EXTRA_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {
        'description': 'Invalid operations',
        'content': {
            'application/json': {
                'examples': {
                    'fullAmountTooLow': {
                        'value': {
                            'detail': (
                                'Нелья установить значение full_amount меньше '
                                'уже вложенной суммы.'
                            )
                        }
                    },
                    'notUniqueName': {
                        'value': {
                            'detail': 'Проект с таким именем уже существует!'
                        }
                    },
                    'projectClosed': {
                        'value': {
                            'detail': 'Закрытый проект нельзя редактировать!'
                        }
                    }
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE,
    status.HTTP_403_FORBIDDEN: FORBIDDEN_RESPONSE,
    status.HTTP_404_NOT_FOUND: NOT_FOUND_RESPONSE
}
CHARITY_PROJECT_DELETE_EXTRA_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {
        'description': (
            'Нельзя удалять закрытый проект или проект, в который уже были '
            'инвестированы средства.'
        ),
        'content': {
            'application/json': {
                'examples': {
                    'projectClosed': {
                        'value': {
                            'detail': (
                                'В проект были внесены средства, не подлежит '
                                'удалению!'
                            )
                        }
                    },
                    'projectWithDonations': {
                        'value': {
                            'detail': (
                                'В проект были внесены средства, не подлежит '
                                'удалению!'
                            )
                        }
                    }
                }
            }
        }
    },
    status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE,
    status.HTTP_403_FORBIDDEN: FORBIDDEN_RESPONSE,
    status.HTTP_404_NOT_FOUND: NOT_FOUND_RESPONSE
}
DONATION_GET_ALL_EXTRA_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE,
    status.HTTP_403_FORBIDDEN: FORBIDDEN_RESPONSE
}
DONATION_CREATE_EXTRA_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE
}
DONATION_GET_MY_EXTRA_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE
}
