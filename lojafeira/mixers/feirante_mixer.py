from mixer.backend.django import mixer
from ..models import Feirante

mixer.cycle(100).blend(Feirante)

