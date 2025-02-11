from django.utils.translation import gettext_lazy as _
from model_utils import Choices

ORDER_STATUS = Choices(
    ('pending', _('Pending')),
    ('completed', _('Completed')),
    ('cancelled', _('Cancelled')),
)