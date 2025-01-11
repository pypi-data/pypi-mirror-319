######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.2.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-08T23:52:28.278380                                                            #
######################################################################################################

from __future__ import annotations

import typing
import abc
if typing.TYPE_CHECKING:
    import abc

from . import secrets_decorator as secrets_decorator
from . import inline_secrets_provider as inline_secrets_provider

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

