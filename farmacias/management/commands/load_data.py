from django.core.management.base import BaseCommand, CommandError
from observaciones.models import Observacion
from protocolos.models import Protocolo
from servicios.models import (
    Servicio
)
from django.contrib.auth.models import User
from colaboradores.models import Colaborador
from clientes.models import Cliente
from farmacias.models import Farmacia
from django.conf import settings
import json
import datetime


class Command(BaseCommand):
    help = "Load Json Data into the database"

    def handle(self, *args, **options):
        self.stdout.write("Loading Json Data")
        user_farmacia = User.objects.create_user(
            username="pablo1234",
            password="pablo1234",
        )
        farmacia = Farmacia(nombre="Yuvone", user=user_farmacia)
        farmacia.save()

        data = []
        with open(settings.BASE_DIR / "data/servicios.json", "r") as rf:
            data.extend(json.load(rf))
            for elem in data:
                row = elem.copy()
                row["farmacia"] = farmacia
                instance = Servicio(**row)
                instance.save()

        data = []
        with open(settings.BASE_DIR / "data/colaboradores.json", "r") as rf:
            data.extend(json.load(rf))
            for elem in data:
                row = elem.copy()
                row["farmacia"] = farmacia
                instance = Colaborador(**row)
                instance.save()

        data = []
        with open(settings.BASE_DIR / "data/clientes.json", "r") as rf:
            data.extend(json.load(rf))
            for elem in data:
                row = elem.copy()
                row["farmacia"] = farmacia
                
                dni = row.pop("dni", 0)
                try:
                    dni = int(dni)
                except Exception as e:
                    dni = 0

                row["dni"] = dni
                instance = Cliente(**row)
                instance.save()

        data = []
        with open(settings.BASE_DIR / "data/protocolos.json", "r") as rf:
            data.extend(json.load(rf))
            for elem in data:
                row = elem.copy()
                row["farmacia"] = farmacia
                cliente = row.pop("cliente")
                dni = cliente.pop("dni", 0)
                try:
                    dni = int(dni)
                    cliente["dni"] = dni
                except Exception as e:
                    pass

                cliente = Cliente.objects.filter(**cliente)
                if cliente.exists():
                    cliente = cliente.first()
                    row["cliente"] = cliente

                servicio = row.pop("servicio")
                servicio = Servicio.objects.filter(**servicio)
                
                if servicio.exists():
                    servicio = servicio.first()
                    row["servicio"] = servicio

                colaborador = row.pop("colaborador")
                colaborador = Colaborador.objects.filter(**colaborador)
                
                if colaborador.exists():
                    colaborador = colaborador.first()
                    row["colaborador"] = colaborador

                fecha = row.pop("fecha")
                if fecha == "":
                    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
                    row["fecha"] = fecha
                else:
                    anio = int(fecha.split("/")[2])
                    mes = int(fecha.split("/")[1])
                    dia = int(fecha.split("/")[0])
                    fecha = datetime.datetime(anio, mes, dia).strftime("%Y-%m-%d")
                    row["fecha"] = fecha

                fecha_vencimento = row.pop("fecha_vencimento")
                if fecha_vencimento == "":
                    fecha_vencimento = datetime.datetime.now().strftime("%Y-%m-%d")
                    row["fecha_vencimento"] = fecha_vencimento
                else:
                    anio = int(fecha_vencimento.split("/")[2])
                    mes = int(fecha_vencimento.split("/")[1])
                    dia = int(fecha_vencimento.split("/")[0])
                    fecha_vencimento = datetime.datetime(anio, mes, dia).strftime("%Y-%m-%d")
                    row["fecha_vencimento"] = fecha_vencimento

                observaciones = row.pop("observaciones")

                for k in row:
                    if row[k] is None:
                        row[k] = 0

                prot = Protocolo(**row)
                prot.save()
                
                obs_instances = []
                for item in observaciones:
                    obs = item.copy()
                    obs_colaborador = obs.pop("colaborador")
                    obs_colaborador = Colaborador.objects.filter(**obs_colaborador)
                    
                    if obs_colaborador.exists():
                        obs_colaborador = obs_colaborador.first()
                        obs["colaborador"] = obs_colaborador

                    obs["farmacia"] = farmacia
                    observacion = Observacion(**obs)
                    observacion.save()
                    obs_instances.append(observacion)

                prot.observaciones.set(obs_instances)
                prot.save()