from django.db import models
from django.contrib.auth.models import User

class EstadoReporte(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    intentos = models.PositiveIntegerField(default=0)
    genera_movimiento = models.BooleanField(default=True) 

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    numero_cliente = models.CharField(max_length=50, unique=True)
    nombre_cliente = models.CharField(max_length=255)
    contacto_cliente = models.CharField(max_length=255)
    telefono_cliente = models.CharField(max_length=50, null=True, blank=True)
    telefono_dos = models.CharField(max_length=50, null=True, blank=True)  
    direccion = models.CharField(max_length=255, null=True, blank=True)    
    correo = models.CharField(max_length=254, null=True, blank=True)     
    estado_actual = models.ForeignKey(EstadoReporte, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    asignado_inicial = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_asignados_inicialmente')
    asignado_usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_asignados')
    veces_contactado = models.PositiveIntegerField(default=0)
    sin_contestar = models.PositiveIntegerField(default=0)
    formulario_sin_contestar = models.PositiveIntegerField(default=0)
    ultima_llamada_no_contesto = models.DateTimeField(null=True, blank=True)
    ultimo_envio_formulario = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.numero_cliente} - {self.nombre_cliente}"


class MovimientoEstado(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='movimientos')
    estado = models.ForeignKey(EstadoReporte, on_delete=models.SET_NULL, null=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.cliente} - {self.estado} @ {self.fecha_hora}"


class NotaMovimiento(models.Model):
    movimiento = models.ForeignKey(MovimientoEstado, on_delete=models.CASCADE, related_name='notas')
    texto = models.CharField(max_length=500)
    fecha_creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota para {self.movimiento} - {self.texto[:30]}..."
    
class HistorialEstadoSinMovimiento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='historial_sin_movimiento')
    estado = models.ForeignKey(EstadoReporte, on_delete=models.SET_NULL, null=True)
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nota = models.CharField(max_length=500, blank=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    genera_movimiento = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.cliente} - {self.estado} ({self.fecha_hora})"
