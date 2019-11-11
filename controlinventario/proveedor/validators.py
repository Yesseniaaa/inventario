from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from itertools import cycle

# Aqui van las validaciones

def ValidateMayorCero(value):
    if value <= 0:
        raise ValidationError(_("El valor no puede ser 0 o negativo"))
    else:
        return value

def ValidateRut(rut):
	rut = rut.upper()
	rut = rut.replace("-","")
	rut = rut.replace(".","")
	aux = rut[:-1]
	dv = rut[-1:]
 
	revertido = map(int, reversed(str(aux)))
	factors = cycle(range(2,8))
	s = sum(d * f for d, f in zip(revertido,factors))
	res = (-s)%11
 
	if str(res) == dv:
		return True
	elif dv=="K" and res==10:
		return True
	else:
		raise ValidationError('Rut invalido')



