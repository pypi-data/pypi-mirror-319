######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.1                                                                                 #
# Generated on 2025-01-06T13:29:15.344821                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

