######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.1.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-06T16:50:32.700758                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ......exception import MetaflowException as MetaflowException

class LoadingException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

class ModelException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, message):
        ...
    ...

