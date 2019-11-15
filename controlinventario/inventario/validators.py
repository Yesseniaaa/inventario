from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from itertools import cycle

def ValidateNumeroPositivo(value):
    if value < 0:
        raise ValidationError(_("El valor no puede negativo"))
    else:
        return value

def ValidateMayorCero(value):
    if value <= 0:
        raise ValidationError(_("El valor no puede ser 0 o negativo"))
    else:
        return value