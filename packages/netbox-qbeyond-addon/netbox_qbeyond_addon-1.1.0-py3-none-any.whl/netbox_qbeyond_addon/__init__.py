from netbox.plugins import PluginConfig


class QBAddonConfig(PluginConfig):
    """
    This class defines attributes for the scanplus Addon plugin.
    """

    # Plugin package name
    name = "netbox_qbeyond_addon"

    # Human-friendly name and description
    verbose_name = "qbeyond Addon"
    description = "Add functions used by qbeyond AG"

    # Plugin version
    version = "1.1.0"

    # Plugin author
    author = "Tobias Genannt"
    author_email = "tobias.genannt@qbeyond.de"

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    default_settings = {}

    # Base URL path. If not set, the plugin name will be used.
    base_url = "qb-addon"

    # Minimun Netbox version
    min_version = "4.2.0"


config = QBAddonConfig
