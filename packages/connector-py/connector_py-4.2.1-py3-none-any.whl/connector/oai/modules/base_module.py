from abc import abstractmethod
from typing import TYPE_CHECKING

from connector.generated import StandardCapabilityName

if TYPE_CHECKING:
    from connector.oai.integration import Integration


class BaseIntegrationModule:
    """
    Base class for all integration modules.
    Integration modules allow you to register "global" capabilities that are not specific to a particular integration.
    """

    capabilities: list[StandardCapabilityName | str] = []

    def add_capability(self, capability: str):
        """Add a capability to the module."""
        self.capabilities.append(capability)

    @abstractmethod
    def register(self, integration: "Integration"):
        """Register all capabilities of the module / the module."""
        pass
