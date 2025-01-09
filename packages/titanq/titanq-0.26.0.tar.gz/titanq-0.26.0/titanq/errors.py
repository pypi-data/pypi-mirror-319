# Copyright (c) 2024, InfinityQ Technology, Inc.

"""
Errors specific to the TitanQ SDK.
"""

class TitanqError(Exception):
    """Base TitanQ error"""

class MissingTitanqApiKey(TitanqError):
    """TitanQ Api key is missing"""

class MissingVariableError(TitanqError):
    """Variable has not already been registered"""

class VariableAlreadyExist(TitanqError):
    """Variable with the same name already exist"""

class MissingObjectiveError(TitanqError):
    """Objective has not already been registered"""

class MaximumConstraintLimitError(TitanqError):
    """The number of constraints is bigger than the number of variables"""

class ConstraintSizeError(TitanqError):
    """The constraint size does not match"""

class ConstraintAlreadySetError(TitanqError):
    """A constraint has already been set"""

class ObjectiveAlreadySetError(TitanqError):
    """An objective has already been set"""

class OptimizeError(TitanqError):
    """Error occur during optimization"""

class ServerError(TitanqError):
    """Error returned by the server"""

class ConnectionError(TitanqError):
    """Error due to a connection issue with an external resource"""

class TautologicalExpressionError(TitanqError):
    """
    Exception raised when an expression is tautological (always true).

    This exception indicates that the provided expression is redundant
    and does not add meaningful constraints or information.
    """
    def __init__(self, message="The provided expression is tautological and always evaluates to True, regardless of the variable values.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class ContradictoryExpressionError(TitanqError):
    """
    Exception raised when an expression is contradictory (always false).

    This exception indicates that the provided expression is invalid
    as it represents an impossible condition.
    """
    def __init__(self, message="The provided expression is contradictory and always evaluates to False, regardless of the variable values.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
