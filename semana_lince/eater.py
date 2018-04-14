import time
import gspread
from django.db import IntegrityError
from oauth2client.service_account import ServiceAccountCredentials

from semana_lince import models


def insert_ponente():
    for actividad in actividad_rows:
        ponente = actividad['nombre_ponentes']
        if ponente != 'PENDIENTE' and ponente != '' and ponente is not None:
            ponentes = ponente.split(',')
            for person in ponentes:
                models.Speaker.objects.get_or_create(name=person)


def insert_responsable():
    for actividad in actividad_rows:
        responsable = actividad['responsable']
        if responsable != 'PENDIENTE' and responsable != '' and responsable is not None:
            models.Responsable.objects.get_or_create(name=responsable)


def insert_ubitacions():
    for row in horarios_rows:
        ubication = row['lugar']
        if ubication != 'PENDIENTE' and ubication != '' and ubication is not None:
            models.Location.objects.get_or_create(name=str(ubication))


def insert_actividad():
    for actividad_data in actividad_rows:
        if actividad_data['nombre_actividad'] != 'PENDIENTE' and actividad_data['nombre_actividad'] != '' and \
                actividad_data['nombre_actividad'] is not None:
            activity = models.Activity()
            activity.pk = actividad_data['num_actividad']
            activity.name = actividad_data['nombre_actividad']
            activity.speaker_material = actividad_data['material_ponente']
            activity.participant_material = actividad_data['material_participante']
            activity.description = actividad_data['descripcion']
            activity.external = True if actividad_data['servicio'].lower() == 'externo' else False

            if actividad_data['tipo']:
                try:
                    activity.activity_type = models.ActivityType.objects.filter(name_icontains=actividad_data['tipo'].strip()).first()
                except Exception:
                    print('AcType', actividad_data['tipo'])

            if actividad_data['categoria']:
                try:
                    activity.category = models.ActivityCategory.objects.filter(name__icontains=actividad_data['categoria']).first()
                except models.ActivityCategory.DoesNotExist:
                    print('categoria', actividad_data['categoria'])

            if actividad_data['responsable']:
                department = None
                try:
                    department = models.Department.objects.filter(name__icontains=actividad_data['responsable']).first()
                except models.Department.DoesNotExist:
                    pass
                if not department:
                    activity.department = models.Department.objects.get(pk=99)
                else:
                    activity.department = department
            else:
                activity.department = models.Department.objects.get(pk=99)

                try:
                    responsable = models.Responsable.objects.filter(name__icontains=actividad_data['responsable']).first()
                    activity.responsable = responsable
                except models.Responsable.DoesNotExist:
                    pass

            activity.save()


def insert_actividad_ponente():
    for actividad in actividad_rows:
        num_actividad = actividad['num_actividad']
        ponente = actividad['nombre_ponentes']
        if ponente != 'PENDIENTE' and ponente != '' and ponente is not None:
            ponentes = ponente.split(',')
            for person in ponentes:
                activity = models.Activity.objects.get(pk=num_actividad)
                events = activity.event_set.all()
                for event in events:
                    event.speakers.add(
                        models.Speaker.objects.get(name=person)
                    )


def insert_horario():
    for horario in horarios_rows:
        if horario['fecha'] != '' and horario['hora_inicio'] != '':
            event = models.Event()
            event.activity_id = horario['num_actividad']
            event.date = time.strftime('%Y-%m-%d', time.strptime(horario['fecha'], '%Y/%m/%d'))
            event.start_at = time.strftime('%H:%M:%S', time.strptime(horario['hora_inicio'], '%H:%M:%S'))
            event.ends_at = time.strftime('%H:%M:%S', time.strptime(horario['hora_final'], '%H:%M:%S'))
            event.location = models.Location.objects.get(name=str(horario['lugar']))
            event.capacity = 30 if horario['capacidad'] == '' else int(horario['capacidad'])
            event.save()


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

doc = client.open("semana_lince_app-7.xlsx")
activ = doc.worksheet("ACTIVIDADES")
horarios = doc.worksheet("HORARIOS")

actividad_rows = activ.get_all_records()
horarios_rows = horarios.get_all_records()

print('=========================>	 P O N E N T E  L O G S 						<=========================')
print('')
insert_ponente()
print('')
print('=========================>	 R E S P O N S A B L E  L O G S 				<=========================')
print('')
insert_responsable()
print('')
print('=========================>	 U B I C A T I O N  L O G S 					<=========================')
print('')
insert_ubitacions()
print('')
print('=========================>	 A C T I V I D A D  L O G S 					<=========================')
print('')
insert_actividad()
print('')
print('')
print('=========================>	 H O R A R I O  L O G S 						<=========================')
print('')
insert_horario()
print('')
print('=========================>	 A C T I V I D A D _ P O N E N T E  L O G S 	<=========================')
print('')
insert_actividad_ponente()
