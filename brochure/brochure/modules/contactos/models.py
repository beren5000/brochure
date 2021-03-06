#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from brochure.settings import DEFAULT_FROM_EMAIL, CONTACT_FORM

# Create your models here.

class Maestra(models.Model):
    nombre=models.CharField(max_length=100,null=False)
    descripcion = models.TextField(blank=True,null=True)
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    activo=models.BooleanField(db_index=True,default=True)
    class Meta:
        ordering = ["nombre",'modificado']
        abstract = True
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Contactos(Maestra):

    email = models.EmailField(verbose_name="Email", max_length=70, unique=True)
    class Meta:
        verbose_name = "Formulario de Contacto"
        verbose_name_plural = "Formulario de Contactos"

    def __unicode__(self):
        return u'%s' % (self.nombre)

class Mensajes(models.Model):
    creado=models.DateTimeField(auto_now_add=True)
    modificado=models.DateTimeField(auto_now=True)
    contacto = models.ForeignKey('Contactos',related_name='info_contactos')
    mensaje = models.TextField(blank=True,null=True)
    organizacion = models.CharField(verbose_name="Organizacion",max_length=100,null=True,blank=True)
    posicion = models.CharField(verbose_name="Posicion en la Organizacion",max_length=100,null=True,blank=True)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __unicode__(self):
        return u'%s' % (self.contacto.nombre)

    def enviar_emails(self):
        send_mail('Nuevo contacto '+self.contacto.nombre, self.mensaje+" Email del Contacto: "+self.contacto.email, self.contacto.email, [CONTACT_FORM], fail_silently=False)


class Newsletter(Maestra):

    template = models.CharField(verbose_name="template",max_length=100,null=True,blank=True)
    subject = models.CharField(max_length=100,null=False)
    text_content = models.TextField(blank=True,null=True)
    enviado = models.BooleanField(db_index=True,default=True)
    contactos = models.ManyToManyField(Contactos)

    def send_newsletter(self):
        html = get_template(self.template)
        for contacto in self.contactos.filter(activo=True):
            d = Context({ 'nombres': contacto.nombre })

            html_content = html.render(d)
            msg = EmailMultiAlternatives(self.subject, html_content, DEFAULT_FROM_EMAIL, [contacto.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

##contactosform
class ContactosForm(ModelForm):
    class Meta:
        model = Contactos
        fields = ['email', 'nombre']

class MensajeInlineForm(ModelForm):
    class Meta:
        model = Mensajes
        fields = ['posicion','organizacion','mensaje']

InlineMensajeFactory = inlineformset_factory(Contactos, Mensajes, form=MensajeInlineForm, can_delete=False, extra=1)

