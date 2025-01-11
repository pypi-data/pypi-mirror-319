######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.2.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-08T23:52:28.315509                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import abc
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.secrets
    import abc

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

