from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.urls import reverse
import uuid
from django.contrib.auth.models import User

from django.utils import timezone


class ClaseModelo(models.Model):
    activo = models.BooleanField(
        default=True, null=True, editable=True)

    creado = models.DateTimeField(
        auto_now_add=True, null=True, editable=True)
    modificado = models.DateTimeField(
        default=timezone.now, null=True, editable=True)

    class Meta:
        abstract = True


class Recurrente(ClaseModelo):
    nombre = models.CharField(max_length=50, unique=True)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    ruc = models.IntegerField(null=True, blank=True)
    rmc = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.apellido:
            return '%s, %s' % (self.nombre, self.apellido)
        else:
            return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Barrio(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


class Calle(models.Model):
    #  TIPO
    EMPEDRADA = 1
    ASFALTADA = 2
    INDETERMINADA = 3
    TIPO_CHOICES = (
        (EMPEDRADA, "Empedrada"),
        (ASFALTADA, "Asfaltada"),
        (INDETERMINADA, "Indeterminada"),)

    #  SENTIDO
    UNICO = 1
    DOBLE = 2
    INDETERMINADO = 3
    SENTIDO_CHOICES = (
        (UNICO, "Unico"),
        (DOBLE, "Doble"),
        (INDETERMINADO, "Indeterminado"),)

    #  NUMERACION
    DERECHA = 1
    IZQUIERDA = 2
    INDETERMINADA = 3
    NUMERACION_CHOICES = (
        (DERECHA, "Derecha"),
        (IZQUIERDA, "Izquierda"),
        (INDETERMINADA, "Indeterminada"),)

    nombre = models.CharField(max_length=50)
    tipo = models.IntegerField(choices=TIPO_CHOICES, null=True, default=2)
    sentido = models.IntegerField(choices=SENTIDO_CHOICES, null=True, blank=True)
    numeracion = models.IntegerField(choices=NUMERACION_CHOICES,
        help_text='Lado numeración viviendas', null=True, blank=True)
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


class Documento_estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Documento_referencia(ClaseModelo):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Documento(ClaseModelo):
    #  SENTIDO
    UNICO = 1
    DOBLE = 2
    SENTIDO_CHOICES = (
        (UNICO, "Unico"),
        (DOBLE, "Doble"),)

    #  CALZADA
    DERECHA = 1
    IZQUIERDA = 2
    CALZADA_CHOICES = (
        (DERECHA, "Derecha"),
        (IZQUIERDA, "Izquierda"),)

    #  CLASE
    EXPEDIENTE = 1
    NOTA = 2
    MEMO = 3
    OFICIO = 4
    FORMULARIO = 5
    CLASE_CHOICES = (
        (EXPEDIENTE, "Expediente"),
        (NOTA, "Nota"),
        (MEMO, "Memo"),
        (OFICIO, "Oficio"),
        (FORMULARIO, "Formulario"),)

    creado_por = models.ForeignKey(
        User, related_name='generado_por', on_delete=models.SET_NULL,
        null=True, blank=True)

    tipo = models.IntegerField(choices=CLASE_CHOICES, default=1)
    nro = models.IntegerField(blank=True, null=True)
    fecha = models.DateField()
    recurrente = models.ForeignKey(Recurrente, null=True, on_delete=models.SET_NULL)
    mesa = models.ForeignKey(
        User, related_name="creado_por", null=True, on_delete=models.SET_NULL, blank=True)
    tecnico = models.ForeignKey(
        User, related_name="asignado_a", null=True, on_delete=models.SET_NULL, blank=True)

    motivo = models.ManyToManyField(
        Documento_referencia, related_name='motivo')
    # , through='Motivo_detalle'

    # calle_principal = models.ForeignKey(
    #     Calle, on_delete=models.CASCADE,
    #     related_name="calle_principal", null=True, blank=True)
    # calzada = models.IntegerField(choices=CALZADA_CHOICES, null=True, blank=True)
    # calle1 = models.ForeignKey(
    #     Calle, on_delete=models.CASCADE, related_name="calle1", null=True, blank=True)
    # calle2 = models.ForeignKey(
    #     Calle, on_delete=models.CASCADE, related_name="calle2", null=True, blank=True)
    # inicio_evento = models.DateTimeField(null=True, blank=True)
    # fin_evento = models.DateTimeField(null=True, blank=True)
    estado = models.ForeignKey(Documento_estado, on_delete=models.CASCADE)
    observacion = models.TextField(help_text='Descripción adicional', null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True)

    def dias(self):
        return self.fecha >= timezone.now() - datetime.timedelta(days=15)
    #  upload_to="/images/"

    # def display_motivo(self):
    #     return ', '.join(
    #         [Documento_motivo.name for Documento_motivo
    #         in self.Documento_motivo.all()[:3]])

    # display_motivo.short_description = 'Motivo'

    @property
    def solo_año(self):
        return self.fecha.strftime('%Y')

    def __str__(self):
        return '%d/%s' % (self.nro, self.solo_año)
        # return '%s, %s' % (self.nro, self.recurrente)

    def get_absolute_url(self):
        return reverse('documento-detalle', args=[str(self.id)])

    class Meta:
        ordering = ["-nro"]
        unique_together = (("nro", "fecha"),)


class DocumentoInstance(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text="ID único para Documento")
    documento = models.ForeignKey(
        'Documento', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s (%s)' % (self.id, self.documento.nro)


class Destino(ClaseModelo):
    nombre = models.CharField(max_length=50, unique=True)
    acronimo = models.CharField(
        max_length=15, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['nombre']
        unique_together = (('nombre', 'acronimo'))


class Documento_mesa(models.Model):
    documento = models.ForeignKey(
        Documento, on_delete=models.CASCADE, null=True)
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mesa = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mesa', null=True)
    destino = models.ForeignKey(
        Destino, on_delete=models.SET_NULL, null=True, blank=True)
    para = models.ForeignKey(
        Destino, related_name='destino_2', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    fecha_registro_mesa = models.DateTimeField(auto_now_add=True)

    recibido = models.BooleanField(default=False)
    fecha_recibido = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.documento

    class Meta:
        ordering = ["-fecha_salida"]


class Evento_tipo(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Cierre_tipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Camiones_tipo(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Herramientas_tipo(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Suelo_tipo(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class Cartel(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.CharField(max_length=50, null=True)


class Informe_clase(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-nombre"]


class InformeResultado(models.Model):
    nombre = models.CharField(max_length=50)
    detalle = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre

class Informe(ClaseModelo):
    # Informe.objects.filter(tipo__nombre="Espacio Reservado").count()
    documento = models.ForeignKey(
        Documento, on_delete=models.CASCADE, null=True)
    DERECHA = 1
    IZQUIERDA = 2
    CALZADA_CHOICES = (
        (DERECHA, "Derecha"),
        (IZQUIERDA, "Izquierda"),)
    nro = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recurrente = models.ForeignKey(
        Recurrente, on_delete=models.CASCADE, null=True)
    resultado = models.ForeignKey(
        InformeResultado, on_delete=models.CASCADE, null=True)

    tipo = models.ManyToManyField(Informe_clase, related_name='clase')
    espacios = models.IntegerField(null=True, blank=True)

    # DIRECCION ---------------------------
    calle_principal = models.ForeignKey(
        Calle, on_delete=models.CASCADE,
        related_name="inf_calle_principal", null=True, blank=True)
    calzada = models.IntegerField(choices=CALZADA_CHOICES, null=True, blank=True)
    calle1 = models.ForeignKey(
        Calle, on_delete=models.CASCADE, related_name="inf_calle_1", null=True, blank=True)
    calle2 = models.ForeignKey(
        Calle, on_delete=models.CASCADE, related_name="inf_calle_2", null=True, blank=True)

    #  -- EVENTOS --
    #  Descripcion de Actividad
    evento_tipo = models.ForeignKey(
        Evento_tipo, on_delete=models.CASCADE, null=True, blank=True)
    #  Evento
    inicio_evento = models.DateTimeField(null=True, blank=True)
    fin_evento = models.DateTimeField(null=True, blank=True)
    personas = models.IntegerField(null=True, blank=True)
    trabajadores = models.IntegerField(null=True, blank=True)
    andamios_m2 = models.IntegerField(null=True, blank=True)
    tarimas_m2 = models.IntegerField(null=True, blank=True)
    #  Obras
    vallados_m2 = models.IntegerField(null=True, blank=True)
    vallados_altura = models.IntegerField(null=True, blank=True)
    vallados_superficie = models.IntegerField(null=True, blank=True)
    camiones_total = models.IntegerField(null=True, blank=True)
    camiones_tipo = models.ManyToManyField(Camiones_tipo, blank=True)
    herramientas = models.ManyToManyField(Herramientas_tipo, blank=True)
    suelo = models.ManyToManyField(Suelo_tipo, blank=True)

    # CIERRE DE CALLE
    TOTAL = 1
    PARCIAL = 2
    OTROS = 3
    CIERRE_CHOICES = (
        (TOTAL, "Total"),
        (PARCIAL, "Parcial"),
        (OTROS, "Otros"),)
    cierre = models.BooleanField(null=True, blank=True)
    cierre_de = models.ManyToManyField(Cierre_tipo, blank=True)
    cierre_detalle = models.IntegerField(choices=CIERRE_CHOICES, null=True, blank=True)

    # PMT
    covertura = models.BooleanField(default=False, null=True, blank=True)
    pmt_hora_inicio = models.TimeField(null=True, blank=True)
    pmt_hora_fin = models.TimeField(null=True, blank=True)

    # SEÑALIZACION
    señaletica = models.BooleanField(default=False, null=True, blank=True)
    carteles_total = models.IntegerField(null=True, blank=True)
    cartel_tipo = models.ForeignKey(
        Cartel, on_delete=models.CASCADE, null=True, blank=True)
    cartel_cantidad = models.IntegerField(null=True, blank=True)

    # CONTENEDOR
    contenedor = models.BooleanField(default=False, null=True, blank=True)
    contenedor_cantidad = models.IntegerField(null=True, blank=True)

    #  GIS
    coord_x = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    coord_y = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)

    imagen = models.ImageField(blank=True, null=True)

    observacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.nro, self.usuario)

    def get_absolute_url(self):
        return reverse('informe-detalle', args=[str(self.id)])

    class Meta:
        ordering = ["-nro"]
        # unique_together = (("nro", "documento"),)


class Historial(ClaseModelo):
    #  Tablas
    tabla = models.CharField(max_length=20)
    campo = models.CharField(max_length=20)
    anterior = models.CharField(max_length=20)
    nuevo = models.CharField(max_length=20)

    #  cambios
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Tarea(ClaseModelo):
    nombre = models.CharField(max_length=100)
    creado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='creada_por', null=True)
    designado_a = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='designado_a', null=True)
    fecha = models.DateField(null=True)
    fecha_fin = models.DateField()
    observacion = models.TextField(null=True)
