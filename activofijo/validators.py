from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from itertools import cycle
from datetime import date


# Aqui van las validaciones

def ValidateMayorCero(value):
    if value <= 0:
        raise ValidationError(_("El valor no puede ser 0 o negativo"))
    else:
        return value

def ValidateLength(value):
    if len(value)<=8:
        raise ValidationError ('Número muy corto, debe ser mayor o igual a 8 digitos.')
    else:
        return True



def ValidateRut(rut):
    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == dv:
        return True
    elif dv == "K" and res == 10:
        return True
    else:
        raise ValidationError('Rut inválido')





def validate_dob(value):
    today = date.today()
    eighteen_years_ago = today.replace(year=today.year - 18)
    if not value <= eighteen_years_ago:
        raise ValidationError('Funcionario debe ser mayor de edad')




def ValidarTelefono(value):
    if int(value) > 0 and  len(value)>8:
        return True
    else:
        raise ValidationError(_("El valor no puede ser 0 o negativo o menor a 8 números"))