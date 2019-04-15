from django import forms
from ingenieria.models import Documento, Informe
from bootstrap_datepicker_plus import DatePickerInput


class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Documento

        fields = [
            'tipo',
            'nro',
            'fecha',
            'recurrente',
            'tecnico',
            'motivo',
            # 'calle_principal',
            # 'calle1',
            # 'calle2',
            # 'inicio_evento',
            # 'fin_evento',
            'estado',
            'observacion',
            'imagen',
            'activo',
            # 'creado',
            'modificado',
            # 'mesa',
            'creado_por',
        ]
        labels = {
            'tipo': 'Tipo',
            'nro': 'Número',
            'fecha': 'Fecha',
            'recurrente': 'Recurrente',
            'tecnico': 'Técnico',
            'motivo': 'Motivo',
            # 'calle_principal': 'Calle Principal',
            # 'calle1': 'Calle 1',
            # 'calle2': 'Calle 2',
            # 'inicio_evento': 'Fecha inicio evento',
            # 'fin_evento': 'Fecha fin evento',
            'estado': 'Estado',
            'observacion': 'Observacion',
            'imagen': 'Imagen',
            'activo': 'Activo',
            # 'creado': 'Creado',
            'modificado': 'Modificado',
            # 'mesa': 'Creado por',
            'creado_por': "Creado por",
        }
        widgets = {
            'tipo': forms.Select(
                attrs={'class': 'form-control', 'required': True, 'autofocus': 'autofocus'}),
            'nro': forms.NumberInput(
                attrs={'class': 'form-control', 'required': True}),
            # 'fecha': DatePickerInput(
            #     options={
            #         "format": "DD/MM/YYYY", # moment date-time format
            #         "showClose": True,
            #         "showClear": True,
            #         "showTodayButton": True, }),
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'required': True, 'placeholder': 'mm/dd/aaaa'}),
            'recurrente': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'tecnico': forms.Select(
                attrs={'class': 'form-control', 'required': False}),
            'motivo': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check form-check-inline', 'required': False}),
            # 'calle_principal': forms.Select(
            #     attrs={'class': 'form-control', 'required': True}),
            # 'calle1': forms.Select(
            #     attrs={'class': 'form-control', 'required': False}),
            # 'calle2': forms.Select(
            #     attrs={'class': 'form-control', 'required': False}),
            # 'inicio_evento': forms.DateTimeInput(
            #     attrs={'class': 'form-control', 'required': False, 'placeholder': 'dd/mm/aaaa hh:mm'}),
            # 'fin_evento': forms.DateTimeInput(
            #     attrs={'class': 'form-control', 'required': False, 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'estado': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'observacion': forms.Textarea(
                attrs={'class': 'form-control', 'required': False}),
            'imagen': forms.FileInput(
                attrs={'class': 'form-control-file', 'required': False}),
            'activo': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'disabledTextInput', "readonly": "readonly"}),
            # 'creado': forms.TextInput(
            #     attrs={'class': 'form-control', 'id': 'disabledTextInput', "readonly": "readonly"}),
            'modificado': forms.DateTimeInput(
                attrs={'class': 'form-control', 'id': 'disabledTextInput', "readonly": "readonly"}),
            # 'mesa': forms.TextInput(
            #     attrs={'class': 'form-control', 'id': 'disabledTextInput', "readonly": "readonly"}),
            'creado_por': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'disabledTextInput', "readonly": "readonly"}),
        }


class InformeForm(forms.ModelForm):

    class Meta:
        model = Informe

        fields = [
            #  DATOS BÁSICOS --------
            'nro',
            'recurrente',

            # DIRECCIÓN -------------
            'calle_principal',
            'calle1',
            'calle2',

            #  EVENTO ---------------
            # 'tipo',
            'evento_tipo',
            'personas',
            'trabajadores',
            'andamios_m2',
            'tarimas_m2',
            'vallados_m2',
            'vallados_altura',
            'vallados_superficie',
            'camiones_total',
            'camiones_tipo',
            'herramientas',
            'suelo',

            #  CIERRE DE CALLE -----
            'cierre',
            'cierre_de',
            'cierre_detalle',

            #  COBERTURA ----------
            'covertura',
            'pmt_hora_inicio',
            'pmt_hora_fin',

            #  SEÑALETICA----------
            'señaletica',
            'carteles_total',
            'cartel_tipo',
            'cartel_cantidad',

            #  CONTENEDOR ---------
            'contenedor',
            'contenedor_cantidad',

            #  COORDENADAS -------
            'coord_x',
            'coord_y',

            #  FINAL ------------
            'resultado',
            'usuario',
            'observacion',


        ]

        labels = {
            #  DATOS BÁSICOS --------
            'nro': 'Número',
            'recurrente': 'Recurrente',

            # DIRECCIÓN -------------
            'calle_principal': 'Calle Principal',
            'calle1': 'Calle 1',
            'calle2': 'Calle 2',

            #  EVENTO ---------------
            # 'tipo': 'Tipo',
            'evento_tipo': 'Tipo',
            'personas': 'Cant. Personas',
            'trabajadores': 'Cant. trabajadores',
            'andamios_m2': 'Andamios m2',
            'tarimas_m2': 'Tarimas m2',
            'vallados_m2': 'Vallados m2',
            'vallados_altura': 'Vallados altura',
            'vallados_superficie': 'Vallados superficie',
            'camiones_total': 'Total Camiones',
            'camiones_tipo': 'Camiones Tipo',
            'herramientas': 'Herramientas',
            'suelo': 'Suelo',

            #  CIERRE DE CALLE -----
            'cierre': 'Cierre de Calle',
            'cierre_de': 'Cierre de',
            'cierre_detalle': 'Detalle',

            #  COBERTURA ----------
            'covertura': 'Cobertura PMT',
            'pmt_hora_inicio': 'Inicio',
            'pmt_hora_fin': 'Fin',

            #  SEÑALETICA----------
            'señaletica': 'Señalética',
            'carteles_total': 'Carteles Total',
            'cartel_tipo': 'Cartel Tipo',
            'cartel_cantidad': 'Cartel Cantidad',

            #  CONTENEDOR ---------
            'contenedor': 'Contenedor',
            'contenedor_cantidad': 'Cantidad',

            #  COORDENADAS -------
            'coord_x': 'Coord. X',
            'coord_y': 'Coord. Y',

            #  FINAL ------------
            'resultado': 'Resultado',
            'usuario': 'Técnico',
            'observacion': 'Observación',
        }

        widgets = {
            #  DATOS BÁSICOS --------
            'nro': forms.NumberInput(
                attrs={'class': 'form-control', 'required': True}),
            'recurrente': forms.Select(
                attrs={'class': 'form-control', 'required': True}),

            # DIRECCIÓN -------------
            'calle_principal': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'calle1': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'calle2': forms.Select(
                attrs={'class': 'form-control', 'required': True}),

            #  EVENTO ---------------
            # 'tipo': 'Tipo',
            'evento_tipo': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'personas': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'trabajadores': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'andamios_m2': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'tarimas_m2': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'vallados_m2': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'vallados_altura': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'vallados_superficie': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'camiones_total': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'camiones_tipo': forms.Select(
                attrs={'class': 'form-control', 'required': False}),
            'herramientas': forms.Select(
                attrs={'class': 'form-control', 'required': False}),
            'suelo': forms.Select(
                attrs={'class': 'form-control', 'required': False}),

            #  CIERRE DE CALLE -----
            'cierre': forms.NullBooleanSelect(
                attrs={'class': 'form-control', 'required': False}),
            'cierre_de': forms.Select(
                attrs={'class': 'form-control', 'required': False}),
            'cierre_detalle': forms.Select(
                attrs={'class': 'form-control', 'required': False}),

            #  COBERTURA ----------
            'covertura': forms.NullBooleanSelect(
                attrs={'class': 'form-control', 'required': False}),
            'pmt_hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control', 'required': False}),
            'pmt_hora_fin': forms.TimeInput(
                attrs={'class': 'form-control', 'required': False}),

            #  SEÑALETICA----------
            'señaletica': forms.NullBooleanSelect(
                attrs={'class': 'form-control', 'required': False}),
            'carteles_total': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'cartel_tipo': forms.Select(
                attrs={'class': 'form-control', 'required': False}),
            'cartel_cantidad': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),

            #  CONTENEDOR ---------
            'contenedor': forms.NullBooleanSelect(
                attrs={'class': 'form-control', 'required': False}),
            'contenedor_cantidad': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            #  COORDENADAS -------
            'coord_x': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),
            'coord_y': forms.NumberInput(
                attrs={'class': 'form-control', 'required': False}),

            #  FINAL ------------
            'resultado': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'usuario': forms.TextInput(
                attrs={'class': 'form-control', 'required': True}),
            'observacion': forms.Textarea(
                attrs={'class': 'form-control', 'required': False}),
        }
