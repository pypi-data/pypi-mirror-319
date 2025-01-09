from dcim.views import DeviceListView

from .filters import QBDeviceFilterSet
from .forms import QBDeviceFilterForm


class QBDeviceListView(DeviceListView):
    filterset = QBDeviceFilterSet
    filterset_form = QBDeviceFilterForm
