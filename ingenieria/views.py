from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse_lazy

from .forms import DocumentoForm, InformeForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import generic

# from ingenieria.models import Documento, Documento_referencia, Informe, Informe_clase, Documento_estado, Calle
from ingenieria.models import *

from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'




class SinPrivilegios(PermissionRequiredMixin):
    login_url = 'sin_privilegios'
    raise_exception = False
    redirect_field_name = 'redirecto_to'

    def handle_no_permission(self):
        messages.error(self.request, 'Tu usuario no tiene suficientes privilegios para cargar la opción solicitada. Ingrese con un usuario diferente o póngase en contacto con el administrador')
        # return super(SinPrivilegios, self).handle_no_permission()
        return HttpResponseRedirect(reverse_lazy(self.login_url))


@login_required(login_url='/login/')
def index(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'index.html', {})


@login_required(login_url='/login/')
def panel(request):
    #  DOCUMENTOS ----------------------
    documentos = Documento.objects.all()
    doc_count = documentos.count()

    referencias = Documento_referencia.objects.values('nombre')
    aux = 0
    ref_nombres = []
    for ref in referencias:
        nombre_aux = referencias[aux]['nombre']
        ref_nombres.append(nombre_aux)
        aux += 1

    ref_nombres_dic = {
        i: ref_nombres[i] for i in range(0, len(ref_nombres))}

    #  INFORMES -------------------------
    informes = Informe.objects.all()
    inf_count = informes.count()

    tipos = Informe_clase.objects.values('nombre')
    aux = 0
    tipo_nombres = []
    for ref in tipos:
        nombre_aux = tipos[aux]['nombre']
        tipo_nombres.append(nombre_aux)
        aux += 1

    tipo_nombres_dic = {
        i: tipo_nombres[i] for i in range(0, len(tipo_nombres))}

    #  DATA ----------------------------
    data = {
        'doc_count': doc_count,
        'inf_count': inf_count,
    }

    return render(request, 'panel.html', {
        'data': data,
        'ref_nombres_dic': ref_nombres_dic,
        'tipo_nombres_dic': tipo_nombres_dic, })


def documentos(request):
    documento = Documento.objects.order_by('-fecha')
    # paginator = Paginator(documento, 25)
    # paginate_by = 25
    # tk_vencido = Ticket.objects.order_by('fecha')

    template = loader.get_template('documento_list.html')
    context = {
        'nro': documento,
        'fecha': documento,
        'recurrente': documento,
        'tecnico': documento,
        'motivo': documento,
    }
    return HttpResponse(template.render(context, request))















class DocumentoListView(LoginRequiredMixin, SinPrivilegios, ListView):
    permission_required = 'ingenieria.view_documento'
    model = Documento
    login_url = 'login'
    template_name = 'documento_list.html'
    # paginate_by = 100
    # listado_documentos = Documento.objects.all()

    # def get_queryset(self):
    #     queryset = super(DocumentoListView, self).get_queryset()
    #     return queryset.filter(nro=self.kwargs['nro'])


class DocumentoAddView(SuccessMessageMixin,
                       LoginRequiredMixin, SinPrivilegios, CreateView):
    permission_required = 'ingenieria.add_documento'
    model = Documento
    login_url = 'login'
    template_name = 'documento_form.html'
    form_class = DocumentoForm
    success_url = reverse_lazy('documento_list')
    success_message = 'Documento creado.'

    def form_valid(self, form):
        form.save()
        return super(DocumentoAddView, self).form_valid(form)


class DocumentoEditView(SuccessMessageMixin,
                        LoginRequiredMixin, SinPrivilegios, UpdateView):
    permission_required = 'ingenieria.change_documento'
    model = Documento
    login_url = 'login'
    template_name = 'documento_form.html'
    form_class = DocumentoForm
    success_url = reverse_lazy('documento_list')
    success_message = 'Documento modificado.'


class DocumentoDeleteView(SuccessMessageMixin,
                          LoginRequiredMixin, SinPrivilegios, DeleteView):
    permission_required = 'ingenieria.delete_documento'
    model = Documento
    login_url = 'login'
    context_object_name = 'obj'
    template_name = 'documento_delete.html'
    form_class = DocumentoForm
    success_url = reverse_lazy('documento_list')
    success_message = 'Documento eliminado.'

















class InformeListView(LoginRequiredMixin, SinPrivilegios, ListView):
    permission_required = 'ingenieria.view_informe'
    model = Informe
    context_object_name = 'obj'
    login_url = 'login'
    template_name = 'informe_list.html'
    paginate_by = 100
    # listado_documentos = Documento.objects.all()

    # def get_queryset(self):
    #     queryset = super(DocumentoListView, self).get_queryset()
    #     return queryset.filter(nro=self.kwargs['nro'])


class InformeAddView(SuccessMessageMixin,
                     LoginRequiredMixin, SinPrivilegios, CreateView):
    permission_required = 'ingenieria.add_informe'
    model = Informe
    login_url = 'login'
    template_name = 'informe_form.html'
    form_class = InformeForm
    success_url = reverse_lazy('informe_list')
    success_message = 'Informe creado.'

    def form_valid(self, form):
        form.save()
        return super(InformeAddView, self).form_valid(form)


class InformeEditView(SuccessMessageMixin,
                      LoginRequiredMixin, SinPrivilegios, UpdateView):
    permission_required = 'ingenieria.change_informe'
    model = Informe
    login_url = 'login'
    template_name = 'informe_form.html'
    form_class = InformeForm
    success_url = reverse_lazy('informe_list')
    success_message = 'Informe modificado.'


class InformeDeleteView(SuccessMessageMixin,
                        LoginRequiredMixin, SinPrivilegios, DeleteView):
    permission_required = 'ingenieria.delete_informe'
    model = Informe
    login_url = 'login'
    context_object_name = 'obj'
    template_name = 'informe_delete.html'
    form_class = InformeForm
    success_url = reverse_lazy('informe_list')
    success_message = 'Informe eliminado.'


















#  ------------- ESTADISTICAS -----------------

@login_required(login_url='/login/')
def graficas(request):
    total = Documento.objects.all()

    #  MOTIVOS ----------------------------
    motivos_nombres = Informe_clase.objects.values('id', 'nombre')
    motivos_dic = {}
    cantidad = 0
    for nro in range(len(motivos_nombres)):
        nombre = motivos_nombres[nro]['nombre']
        idd = motivos_nombres[nro]['id']
        cantidad = Informe.objects.filter(tipo=idd).count()
        motivos_dic.update({nombre: cantidad})

    #  DOC ESTADOS -------------------------
    documento_estados = Documento_estado.objects.values('id', 'nombre')
    estados_dic = {}
    for nro in range(len(documento_estados)):
        estado = documento_estados[nro]['nombre']
        idd = documento_estados[nro]['id']
        cantidad = Documento.objects.filter(estado=idd).count()
        estados_dic.update({estado: cantidad})

    #  DOCUMENTACIONES ---------------------
    expediente = 0
    nota = 0
    memo = 0
    oficio = 0
    formulario = 0
    for nro in range(len(total)):
        if total[nro].tipo == 1:
            expediente += 1
        elif total[nro].tipo == 2:
            nota += 1
        elif total[nro].tipo == 3:
            memo += 1
        elif total[nro].tipo == 4:
            oficio += 1
        elif total[nro].tipo == 5:
            formulario += 1

    #  TECNICOS -----------------------------------
    informe_usuario = Informe.objects.values('usuario')
    user_id = User.objects.values('id', 'username')
    tecnicos_dic = {}

    for nro in range(len(user_id)):
        user = User.objects.get(id=nro + 1)

        if user.has_perm('ingenieria.add_informe'):
            id_tecnico = user.id
            nombre_tecnico = user.username

            tecnico = informe_usuario.filter(usuario=id_tecnico)
            cantidad = tecnico.count()

            tecnicos_dic.update({nombre_tecnico: cantidad})

    data = {
        #  Documentos
        "expediente": expediente,
        "nota": nota,
        "memo": memo,
        "oficio": oficio,
        "formulario": formulario,
        "total": total,
    }

    return render(request, 'graficas.html', {
        'data': data,
        'tecnicos_dic': tecnicos_dic,
        'motivos_dic': motivos_dic,
        'estados_dic': estados_dic,
        })


@login_required(login_url='/login/') # terminar
def graficas_espacios(request):
    inf_espacios = Informe.objects.filter(tipo=2)
    tot_espacios = 0

    for nro in range(len(inf_espacios)):
        esp = inf_espacios[nro].espacios
        tot_espacios += esp

    data = {
        #  Documentos
        "expediente": expediente,
    }

    return render(request, 'graficas_espacios.html', {
        'data': data,
        })


@login_required(login_url='/login/')
def tablas(request):
    total = Documento.objects.all()

    #  MOTIVOS ----------------------------
    motivos_nombres = Informe_clase.objects.values('id', 'nombre')
    motivos_dic = {}
    cantidad = 0
    for nro in range(len(motivos_nombres)):
        nombre = motivos_nombres[nro]['nombre']
        idd = motivos_nombres[nro]['id']
        cantidad = Informe.objects.filter(tipo=idd).count()
        motivos_dic.update({nombre: cantidad})

    #  DOC ESTADOS -------------------------
    documento_estados = Documento_estado.objects.values('id', 'nombre')
    estados_dic = {}
    for nro in range(len(documento_estados)):
        estado = documento_estados[nro]['nombre']
        idd = documento_estados[nro]['id']
        cantidad = Documento.objects.filter(estado=idd).count()
        estados_dic.update({estado: cantidad})

    #  DOCUMENTACIONES ---------------------
    expediente = 0
    nota = 0
    memo = 0
    oficio = 0
    formulario = 0
    for nro in range(len(total)):
        if total[nro].tipo == 1:
            expediente += 1
        elif total[nro].tipo == 2:
            nota += 1
        elif total[nro].tipo == 3:
            memo += 1
        elif total[nro].tipo == 4:
            oficio += 1
        elif total[nro].tipo == 5:
            formulario += 1

    #  TECNICOS -----------------------------------
    informe_usuario = Informe.objects.values('usuario')
    user_id = User.objects.values('id', 'username')
    tecnicos_dic = {}

    for nro in range(len(user_id)):
        user = User.objects.get(id=nro + 1)

        if user.has_perm('ingenieria.add_informe'):
            id_tecnico = user.id
            nombre_tecnico = user.username

            tecnico = informe_usuario.filter(usuario=id_tecnico)
            cantidad = tecnico.count()

            tecnicos_dic.update({nombre_tecnico: cantidad})

    #  ESPACIOS RESERVADOS -----------------------
    # 1 obras
    # 2 espacios
    # 3 cierres
    informes = Informe.objects.filter(tipo=2).prefetch_related().order_by('calle_principal')
    espacios_dic = {}
    lista = []

    for nro in range(len(informes)):
        informe = informes[nro].nro
        calle_aux = informes[nro].calle_principal
        calle1_aux = informes[nro].calle1
        calle2_aux = informes[nro].calle2
        espacios = informes[nro].espacios
        recurrente = informes[nro].recurrente
        documentos = informes[nro].documento

        lista_aux = [
            'nro', informe,
            'principal', calle_aux,
            'calle1', calle1_aux,
            'calle2', calle2_aux,
            'espacios', espacios,
            'recurrente', recurrente,
            'documentos', documentos,
        ]

        lista.append(lista_aux)

    espacios_dic = {i: lista[i] for i in range(0, len(lista))}

    data = {
        #  Documentos
        "expediente": expediente,
        "nota": nota,
        "memo": memo,
        "oficio": oficio,
        "formulario": formulario,
        "total": total,
    }

    return render(request, 'tablas.html', {
        'data': data,
        'tecnicos_dic': tecnicos_dic,
        'motivos_dic': motivos_dic,
        'estados_dic': estados_dic,
        'espacios_dic': espacios_dic,
        })


@login_required(login_url='/login/')
def tabla_espacios(request):
    #  ESPACIOS RESERVADOS -----------------------
    # 1 obras
    # 2 espacios
    # 3 cierres
    informes = Informe.objects.filter(tipo=2).prefetch_related().order_by('calle_principal')
    espacios_dic = {}
    lista = []

    for nro in range(len(informes)):
        informe = informes[nro].nro
        calle_aux = informes[nro].calle_principal
        calle1_aux = informes[nro].calle1
        calle2_aux = informes[nro].calle2
        espacios = informes[nro].espacios
        recurrente = informes[nro].recurrente
        documentos = informes[nro].documento

        lista_aux = [
            'nro', informe,
            'principal', calle_aux,
            'calle1', calle1_aux,
            'calle2', calle2_aux,
            'espacios', espacios,
            'recurrente', recurrente,
            'documentos', documentos,
        ]

        lista.append(lista_aux)

    espacios_dic = {i: lista[i] for i in range(0, len(lista))}

    return render(request, 'espacios_reservados.html', {
        'espacios_dic': espacios_dic,
        })


@login_required(login_url='/login/')
def tabla_calles(request):
    calles = Calle.objects.all().select_related('barrio')
    calles_dic = {}
    lista = []

    for nro in range(len(calles)):
        idd = calles[nro].id
        nombre = calles[nro].nombre
        
        tipo_aux = calles[nro].tipo
        tipo = ''
        if tipo_aux == 1:
            tipo = 'Empedrada'
        elif tipo_aux == 2:
            tipo = 'Asfaltada'
        elif tipo_aux == 3:
            tipo = 'Indeterminada'

        sentido_aux = calles[nro].sentido
        sentido = ''
        if sentido_aux == 1:
            sentido = 'Unico'
        elif sentido_aux == 2:
            sentido = 'Doble'
        elif sentido_aux == 3:
            sentido = 'Indeterminado'

        numeracion_aux = calles[nro].numeracion
        numeracion = ''
        if numeracion_aux == 1:
            numeracion = 'Derecha'
        elif numeracion_aux == 2:
            numeracion = 'Izquierda'
        elif numeracion_aux == 3:
            numeracion = 'Indeterminada'

        barrio = calles[nro].barrio

        lista_aux = [
            'id', idd,
            'nombre', nombre,
            'tipo', tipo,        # choices
            'sentido', sentido,  # choices
            'numeracion', numeracion,   # choices
            'barrio', barrio,    # fk
        ]

        lista.append(lista_aux)

    calles_dic = {i: lista[i] for i in range(0, len(lista))}

    return render(request, 'calles.html', {
        'calles_dic': calles_dic,
        })


@login_required(login_url='/login/')
def tabla_recurrentes(request):
    recurrentes = Recurrente.objects.all()
    recurrentes_dic = {}
    lista = []

    for nro in range(len(recurrentes)):
        idd = recurrentes[nro].id
        nombre = recurrentes[nro].nombre
        apellido = recurrentes[nro].apellido
        email = recurrentes[nro].email
        telefono = recurrentes[nro].telefono
        ruc = recurrentes[nro].ruc
        rmc = recurrentes[nro].rmc

        def none_sense(var):
            if var is None:
                return "-"
            else:
                return var

        idd = none_sense(idd)
        nombre = none_sense(nombre)
        apellido = none_sense(apellido)
        email = none_sense(email)
        telefono = none_sense(telefono)
        ruc = none_sense(ruc)
        rmc = none_sense(rmc)


        lista_aux = [
            'id', idd,
            'nombre', nombre,
            'apellido', apellido,
            'email', email,
            'telefono', telefono,
            'ruc', ruc,
            'rmc', rmc, ]

        lista.append(lista_aux)

    recurrentes_dic = {i: lista[i] for i in range(0, len(lista))}

    return render(request, 'recurrentes.html', {
        'recurrentes_dic': recurrentes_dic,
        })

@login_required(login_url='/login/')
def gis(request):
    informes = Informe.objects.values('nro',
        'tipo', 'documento', 'usuario', 'inicio_evento', 'fin_evento', 'espacios', 'coord_x', 'coord_y', 'resultado')
    evento_prueba = []
    eventos_dic = {}
    tipo = ''

    for num in range(len(informes)):
        nro = informes[num]['nro']
        tipo_aux = informes[num]['tipo']
        documento = informes[num]['documento']
        tecnico = informes[num]['usuario']
        espacios = informes[num]['espacios']
        coord_x = informes[num]['coord_x']
        coord_y = informes[num]['coord_y']
        tecnico_str = ''
        resultado = informes[num]['resultado']

        if resultado == 1:
            #  Documento Tipo ----------------
            if tipo_aux == 1:
                tipo = 'cierre'
                desc = 'Cierre de Calle'
            elif tipo_aux == 2:
                tipo = 'espacio'
                desc = 'Espacio Reservado'

            #  Inicio y Fin de evento --------
            if informes[num]['inicio_evento']:
                inicio_aux = informes[num]['inicio_evento']
                inicio = datetime.strftime(inicio_aux, '%b %d, %Y')
            else:
                inicio = '-'

            if informes[num]['fin_evento']:
                fin_aux = informes[num]['fin_evento']
                fin = datetime.strftime(fin_aux, '%b %d, %Y')
            else:
                fin = '-'

            #  Técnico -------------------------
            if tecnico == 2:
                tecnico_str = 'Lucas'
            elif tecnico == 3:
                tecnico_str = 'Lezcano'

            #  Descripción ----------------------
            if tipo_aux == 2:  # Espacios Reservados
                descripcion = 'Tipo: {}.\
                    Informe: {}.\
                    Espacios: {}.\
                    Técnico: {}.'.format(desc, nro, espacios, tecnico_str)
            else:
                descripcion = 'Tipo: {}.\
                    Informe: {}.\
                    Técnico: {}.\
                    Inicio: {}.\
                    Fin: {}.'.format(desc, nro, tecnico_str, inicio, fin)

            lista = [
                'nro', nro,
                'tipo', tipo,
                'documento', documento,
                'inicio', inicio,
                'fin', fin,
                'tecnico', tecnico_str,
                'coord_x', coord_x,
                'coord_y', coord_y,
                'descripcion', descripcion,
                'espacios', espacios,
            ]

            # eventos_dic.update(evento)
            evento_prueba.append(lista)

    eventos_dic = {i: evento_prueba[i] for i in range(0, len(evento_prueba))}

    # evento1_lat = '-25.303783'
    # evento1_long = '-57.559861'
    # evento1_dett = 'OBRAS: Expediente: 0001/2019. Técnico: William. Fecha:11/03/2019 al 12/03/2019'

    # data = {
    #     'evento1_lat': evento1_lat,
    #     'evento1_long': evento1_long,
    #     'evento1_dett': evento1_dett,
    # }

    return render(request, 'gis.html', {'eventos_dic': eventos_dic})


@login_required(login_url='/login/')
def gis_taxis(request):
    pass

class HomeSinPrivilegios(generic.TemplateView):
    template_name = 'sin_privilegios.html'


def imp_csv():
    with open("F:/recurrentes.csv", 'r') as f:
        # dialect='excel' quotechar=" ' "
        reader = csv.DictReader(f, delimiter=';')
        # pk_aux = Recurrente.objects.latest('pk').pk
        # pk=pk_aux+1

        for row in reader:
            _, created = Recurrente.objects.get_or_create(
                id=row['id'],
                activo=row['activo'],
                creado=row['creado'],
                modificado=row['modificado'],
                nombre=row['nombre'],)

def csv_docs():
    import csv
    with open("F:/docs.csv", 'r') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            if row['nro']:
                nro = row['nro']
                foo, created = Documento.objects.get_or_create(
                    id=row['id'],
                    activo=row['activo'],
                    creado=row['creado'],
                    modificado=row['modificado'],
                    tipo=row['tipo'],
                    nro=nro,
                    fecha=row['fecha'],
                    observacion=row['observacion'],
                    # imagen=row['tipo'],
                    estado_id=row['estado_id'],
                    # mesa_id=row['tipo'],
                    recurrente_id=row['recurrente_id'],
                    # tecnico_id=row['tecnico_id'],
                    # creado_por_id=creado_aux,
                    )
            else:
                foo, created = Documento.objects.get_or_create(
                    id=row['id'],
                    activo=row['activo'],
                    creado=row['creado'],
                    modificado=row['modificado'],
                    tipo=row['tipo'],
                    fecha=row['fecha'],
                    observacion=row['observacion'],
                    # imagen=row['tipo'],
                    estado_id=row['estado_id'],
                    # mesa_id=row['tipo'],
                    recurrente_id=row['recurrente_id'],
                    # tecnico_id=row['tecnico_id'],
                    # creado_por_id=creado_aux,
                    )

            foo.motivo.add(row['motivo'])


def imp_barrio():
    barrios_list = [
        'Banco San Miguel',
        'Bañado Cará Cará',
        'Obrero',
        'Bella Vista',
        'Botánico',
        'Campo Grande',
        'Cañada del Ybyray',
        'Ciudad Nueva',
        'Dr. Francia',
        'La Encarnación',
        'General Caballero',
        'General Díaz',
        'Herrera',
        'Hipódromo',
        'Itá Enramada',
        'Itá Pytã Punta',
        'Jara',
        'Carlos A. López',
        'La Catedral',
        'Las Lomas',
        'Loma Pytá',
        'Los Laureles',
        'Madame Lynch',
        'Manorá',
        'Mariscal Estigarribia',
        'Mariscal López',
        'Mbocayaty',
        'Mburicaó',
        'Mburucuyá',
        'Las Mercedes',
        'Nazareth',
        'Ñu Guazú',
        'Pettirossi',
        'Pinozá',
        'Roberto L. Pettit',
        'Recoleta',
        'Republicano',
        'Ricardo Brugada',
        'Sajonia',
        'Salvador del Mundo',
        'San Antonio',
        'San Blas',
        'San Cristóbal',
        'San Jorge',
        'San Pablo',
        'San Rafael',
        'San Roque',
        'San Vicente',
        'Santa Ana',
        'Santa María',
        'Santa Rosa',
        'Santísima Trinidad',
        'Santo Domingo',
        'Tablada Nueva',
        'Tacumbú',
        'Tembetary',
        'Terminal',
        'Villa Aurelia',
        'Villa Morra',
        'Virgen de Fátima',
        'Virgen de la Asunción',
        'Virgen del Huerto',
        'Vista Alegre',
        'Ycuá Satí',
        'Ytay',
        'Zeballos Cué']

    for b in range(len(barrios_list)):
        #print(barrios_list[b])
        Barrio.objects.create(nombre=barrios_list[b])

def imp_recurr():
    recurr_list = [
        [157, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'G2 S.A.'],
        [158, 't', '12:00:00.000000-04', '2019-04-01 12:00', '(A.P.A.)'],
        [159, 't', '12:00:00.000000-04', '2019-04-01 12:00', '222 S.A.'],
        [160, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Abog. Bernardino Martínez'],
        [161, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Abog. Dionisio Mereles Verón'],
        [162, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Abog. Iris Almada González de Pirovano'],
        [163, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Abog. Nelly Cabrera Boggino'],
        [164, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Abog. Roque Walter Troche'],
        [165, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AC DESARROLLOS GASTRONOMICOS S.A.'],
        [166, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Acciona BTD'],
        [167, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ACECEPB'],
        [168, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Adriana Juana Maria Romañach de Mercado'],
        [169, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Adriana Patricia González Flor'],
        [170, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AFEMEC'],
        [171, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AGB CONSTRUCTORA S.A.'],
        [172, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AGRO INDUSTRIAL Y COMERCIAL PARIS S.A.'],
        [173, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AGROVET S.A.'],
        [174, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Aida Antonia Casco Díaz'],
        [175, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Aida Elisa Peran de Ferreira Da Costa Amarilla'],
        [176, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ALAMEDA S.A.'],
        [177, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ALES S.A.'],
        [178, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Alexander Vomel Falcon'],
        [179, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Alfredo Altarrui'],
        [180, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Alicia Carolina Rivarola Arguello'],
        [181, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Alicia Galeano'],
        [182, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Alicia Susana Fernández Caballero'],
        [183, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Almacén Digital de Oliver Esperanza'],
        [184, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ALTATEC S.A.'],
        [185, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Álvaro David Aguilera Santander'],
        [186, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Amparo Maura Samaniego Vda. De Paciello'],
        [187, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ana Bella Ledesma'],
        [188, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ana Claudia Josefina González de Peralta'],
        [189, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ana Lorena Romero Caballero'],
        [190, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ana Maria Juanita Mendoza de Acha'],
        [191, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ana Maria Sosa De Fernández'],
        [192, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Andrea Carolina Estigarribia y Guillermo Luis Hansen Figueredo'],
        [193, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Andrea Saba Rodríguez'],
        [194, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ANDRES H. ARCE S.A.'],
        [195, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Andrés Sung Uk Kim Lee'],
        [196, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ANEAES'],
        [197, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ángel Báez González'],
        [198, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ángel Gustavo Arietti Gamarra'],
        [199, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Aníbal Germán Zelada Fischer'],
        [200, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Aníbal Leopoldo Cardozo Fleytas'],
        [201, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Antoliano Ruiz Díaz Franco'],
        [202, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Antonia Valentina González de Caballero'],
        [203, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Antonio Delvalle Cantero'],
        [204, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'APESA'],
        [205, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ARAR S.R.L.'],
        [206, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AREA INMOBILIARIA S.R.L.'],
        [207, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ARIES TRAVEL S.A.'],
        [208, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Arnaldo Cecilio Lataza Velázquez'],
        [209, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Arnoldo Wiens Durken'],
        [210, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Arq. Ana Heyn'],
        [211, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Arq. Carla Linares'],
        [212, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Arq. Francisco Cabrera Cordero'],
        [213, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Arq. Pedro Oviedo'],
        [214, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ARTEFACTO S.A.'],
        [215, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ARTES GRAFICAS SOLANO S.R.L.'],
        [216, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ASOCIACION DE POLICIAS VICTIMAS DEL GOLPE DE ESTADO'],
        [217, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ASOCIACION DEL COLEGIO INTERNACIONAL'],
        [218, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Asociación Hijas de San Pablo del Paraguay'],
        [219, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ASTRO S.A.'],
        [220, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ASUNCION RESIDENCIAL S.A.'],
        [221, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AT 2000 S.A.'],
        [222, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Atilio Ale Cabrera'],
        [223, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Atilio Osvaldo Cañete Guillen'],
        [224, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Aurea Lobo de Ricciardi'],
        [225, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AUTOMOTORES Y MAQUINARIAS S.A.E.C.A.'],
        [226, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'AZ INVERSIONES S.A.'],
        [227, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BANCO DE LA NACION ARGENTINA'],
        [228, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BANCO FAMILIAR S.A.E.C.A.'],
        [229, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BANCO FAMILIAR S.A.E.C.A.'],
        [230, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BANCO INTERAMERICANO DE DESARROLLO'],
        [231, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BANCOP S.A.'],
        [232, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BCN CONTRUCCIONES S.A.'],
        [233, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BELLINI S.A.'],
        [234, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Benita Arrua de Ramos'],
        [235, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Benito Vera Lopez'],
        [236, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Berta Maria Alejandra Davalos Yegros y Juan Jose Ruiz Diaz Quintana '],
        [237, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BETHANIA VIAJES Y TURISMO S.A.'],
        [238, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BIENES INMOBILIARIOS S.A.'],
        [239, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Blanca Luz Paniagua de Ferreira'],
        [240, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Blanca Nimia Cano de Siri'],
        [241, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BODY CLUB S.R.L.'],
        [242, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'BRABEN S.R.L.'],
        [243, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Byung Pyu Jun'],
        [244, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'C.C.I. S.A.'],
        [245, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'C.E.D.I. CRECER JUGANDO'],
        [246, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CADENA FARMACENTER S.A.'],
        [247, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Caja de Jubilaciones y Pensiones de la Ande'],
        [248, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Caja Medica y de Profesionales Universitarios'],
        [249, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cansejal Javier Pintos'],
        [250, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CAÑAS PARAGUAYAS S.A.'],
        [251, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CAPILLA LA ROCA'],
        [252, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CARACAL S.A.'],
        [253, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Carlos Alberto Sosa Jovellanos Arias'],
        [254, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Carlos Fernando Jasi'],
        [255, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Carlos Otilio Espinola Bogarin'],
        [256, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Carlos Travieso Romero'],
        [257, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CARPOLU S.A.'],
        [258, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CASA ENRIQUE MATALON S.A.'],
        [259, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CASA GARCETE S.R.L.'],
        [260, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CASA SAMUDIO S.R.L.'],
        [261, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Catalino Caballero Ortega'],
        [262, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Causa N° 1562/18 - Victor Eduardo Vera Cabrera S/Homicidio Culposo'],
        [263, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Celedonia Irene Figueredo Gimenez'],
        [264, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CENTRO CULTURAL LA CHISPA'],
        [265, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CENTRO DE DESPACHANTE DE ADUANAS DEL PARAGUAY'],
        [266, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Centro Educativo Cristiano Canaan'],
        [267, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Centro Educativo Infantil N° 7864'],
        [268, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CENTRO PEDIATRICO INTEGRAL RIERA S.R.L.'],
        [269, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CERROS Y PALMERAS S.A.'],
        [270, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cesar Daniel Gavilan Caballero'],
        [271, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cesar Guillermo Cruz Roa'],
        [272, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CHARLOTTE S.A.'],
        [273, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Chulamit Estrella Chenca de Arditi'],
        [274, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CIPESA'],
        [275, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Circulo de Oficiales de la Fuerza Armada de la Nacion'],
        [276, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CIRCULO DE OFICIALES RETIRADOS DE LA FUERZA ARMADA DE LA NACION'],
        [277, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Circulo de Oficiales Retirados de las Fuerzas Armadas de la Nacion'],
        [278, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CITIBANK N.A. SUCURSAL PARAGUAY'],
        [279, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Claudia Ferreira Duarte'],
        [280, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Claudio Rene Roman Alvarenga'],
        [281, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CLINICA SISUL'],
        [282, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CLUB CENTENARIO'],
        [283, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CLUB GUARANI'],
        [284, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COLEGIO DE ABOGADOS DEL PARAGUAY'],
        [285, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COLEGIO DE ESCRIBANOS DEL PARAGUAY'],
        [286, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COLEGIO DEL SOL'],
        [287, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COLEGIO NACIONAL LAS MERCEDES'],
        [288, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COLONIAL APART S.A.'],
        [289, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COMERCIAL E INDUSTRIAL DEL PARANA S.A.E.C.A.'],
        [290, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Comision Vecinal'],
        [291, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Comision Vecinal "Jardin de la Bahia"'],
        [292, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Comision Vecinal VILLA CORINA'],
        [293, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COMPAÑÍA ADMINISTRADORA DE RIESGO S.A. (CARSA)'],
        [294, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COMPAÑÍA DE DESARROLLO INMOBILIARIO S.A.'],
        [295, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COMPAÑÍA QUIMICA VICENTE SCAVONE'],
        [296, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Alvaro Grau'],
        [297, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Antonio Gaona'],
        [298, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Elvio Segovia'],
        [299, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Federico Franco Troche'],
        [300, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Felix Ayala'],
        [301, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Gabriel Calonga'],
        [302, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Ireneo Roman'],
        [303, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Javier Pintos'],
        [304, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Jose Alvarenga'],
        [305, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Oscar Rodriguez'],
        [306, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejal Victor Hugo Menacho'],
        [307, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejala Elena Alfonsi'],
        [308, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejala Fabiana Benegas'],
        [309, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejala Josefina Kostianovsky'],
        [310, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejala Karen Forcado'],
        [311, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejala Rosanna Rolon'],
        [312, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Concejala Sandra Benitez Albavi'],
        [313, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CONFITERIA GERMANIA'],
        [314, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Congreso Nacional'],
        [315, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CONSORCIO DE COPROPIETARIOS DEL EDIFICIO SANTA MARIA'],
        [316, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CONSTRUCTORA E INMOBILIARIA DEL PARAGUAY S.A. (CININPA S.A.)'],
        [317, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CONSULADO DE POLONIA'],
        [318, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COOPERATIVA COOPEMEC LTDA.'],
        [319, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COOPERATIVA MEDALLA MILAGROSA LTDA.'],
        [320, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COOPERATIVA MULTIACTIVA BARRIOJARENSE DE AHORRO Y CREDITO LTDA'],
        [321, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COOPERATIVA NTRA. SRA. DEL CARMEN LTDA.'],
        [322, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cooperativa Universitaria Ltda.'],
        [323, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COORD. DE FUNC. PUBLICOS Y JUBILADOS Y ACTIVOS'],
        [324, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'COPACO'],
        [325, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Corina Evangelista Dujak de Royg'],
        [326, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CREDI EFECTIVO S.A.'],
        [327, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CREDICITY S.A.'],
        [328, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CREDITO AMIGO S.A.'],
        [329, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cristina Del Puerto'],
        [330, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cristina Magdalena Valenzuela de Velazquez'],
        [331, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Cristina Maria Jure Urrutia'],
        [332, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'CUERPO DE BOMBEROS VOLUNTARIOS DEL PY'],
        [333, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'D & V MEDIFARMA S.A.'],
        [334, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DALIA S.A.C.I.'],
        [335, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Daniel Carlos Zanon'],
        [336, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Daniel Niekammer'],
        [337, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Dario Ramon Caballero Bracho'],
        [338, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DE CONSTRUCTORA'],
        [339, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DE CONSTRUCTORA S.A.'],
        [340, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Defensor Municipal'],
        [341, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DEFENSORIA MUNICIPAL DE ASUNCION'],
        [342, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DELTA INGENIERIA S.R.L.'],
        [343, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DENTAL GUARANI S.A.'],
        [344, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Diego Balanovsky Balbuena'],
        [345, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Diego Ivan Ruiz Diaz Gamarra'],
        [346, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Dila Beatriz Gonzalez Fernandez'],
        [347, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DINATALE S.R.L.'],
        [348, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Direccion de Transito y Transporte'],
        [349, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Direccion General de Gabinete'],
        [350, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DIRECCION NACIONAL DE CORREOS DEL PARAGUAY'],
        [351, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DISTRIBUIDORA CENTRAL S.A.'],
        [352, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DISTRIBUIDORA LA POLICLINICA S.A.'],
        [353, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DISTRISAN S.R.L.'],
        [354, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Dr. Augusto Encina Perez'],
        [355, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Dr. Ivan Allende'],
        [356, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DULCE HOGAR S.R.L.'],
        [357, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'DXV MEDIFARMA S.A.'],
        [358, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EBERHARD LEWKOWITZ S.A.L.'],
        [359, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Edgar Javier Gonzalez Barchello'],
        [360, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Edgar Ruben Vera y Aragon Rodriguez'],
        [361, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EDIFICIO IBIZA'],
        [362, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EDITORA LITOCOLOR S.R.L.'],
        [363, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EFA DISTRIBUIDORA'],
        [364, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Elba Marisol Alarcon Cespedes'],
        [365, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ELECTRO SYSTEM S.R.L.'],
        [366, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ELECTROCENTER S.A.'],
        [367, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ELECTROMACH S.A.'],
        [368, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Elena Diomedes Hirsch Delgado'],
        [369, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Elena Esmilce Martinez Acosta'],
        [370, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ELIAS A. SABA S.A. INMOBILIARIA'],
        [371, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Elsa Edith Monte de Altamirano'],
        [372, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EMBAJADA DE ESPAÑA'],
        [373, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EMBAJADA DE ITALIA'],
        [374, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Emilia Carolina Veron Arce'],
        [375, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Emilio Ramon Guillen Gamarra'],
        [376, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Enio Anibal Varela Veron'],
        [377, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Enrique Gustavo Arbo Seitz'],
        [378, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Eric Nicolas Monnin Fernandez'],
        [379, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Erich Michel Wihr'],
        [380, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Esmeria Sofia Roca de Osorio'],
        [381, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Esperanza Graciela Mayor Martinez'],
        [382, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ESSEN S.R.L.'],
        [383, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Esteban Enrique Tonina Faiman'],
        [384, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Esteban Vera'],
        [385, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Estela Concepcion Berino Samaniego'],
        [386, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'EXPRESAME S.A.'],
        [387, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ezequiel Garcia Rubin'],
        [388, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'F&A S.A.'],
        [389, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'F.A.O. Paraguay'],
        [390, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FACULTAD DE DERECHO Y CIENCIAS SOCIALES'],
        [391, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Facultad de Instrumentacion UNA'],
        [392, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FACULTAD DE INSTRUMENTACION Y AREA QUIRURGICA'],
        [393, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FACULTAD DE ODONTOLOGIA U.N.A'],
        [394, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Farid Elias Id Lemir'],
        [395, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FASHION LADY S.R.L.'],
        [396, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Fatima Carolina Diaz Aguilera'],
        [397, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Felix Lexcano Benitez'],
        [398, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Fernando Jose Cibils Sacarello'],
        [399, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FERRARI CELL S.A.'],
        [400, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FINE S.A.'],
        [401, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Flora Guadalupe Rojas Ortigoza'],
        [402, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FORTALEZA S.A. DE INMUEBLES'],
        [403, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Francisca Ruiz Diaz de Lovera'],
        [404, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Francisca Zaida Fernandez Marecos'],
        [405, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Francisco Arnaldo Ortiz'],
        [406, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Francisco Daniel Alonso Espinola'],
        [407, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FUNDACION NICOLAS LATOURRETTE BO'],
        [408, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FUNDACION PAI PUKU'],
        [409, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FUNDACION PARA LA EDUCACION Y ALIMENTACION AMERICA DEL SUR PY'],
        [410, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FUNDACION TELETON'],
        [411, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'FUNDACIONES ESPECIALES S.A.'],
        [412, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'G.R. CONSULTORA S.A.'],
        [413, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GALANA S.R.L.'],
        [414, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GEOSTAN'],
        [415, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Gerardo Luis Acosta Perez'],
        [416, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GIMENEZ CALVO S.A.C.'],
        [417, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GIMNASIO MARTHA AVILES'],
        [418, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GIPSI NOVIAS'],
        [419, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Gladys Ofelia Esquivel de Cocco'],
        [420, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GLOBO IMPORT EXPORT S.A.'],
        [421, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Gloria Elizabeth Villalba Godoy'],
        [422, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GONZALEZ GIMENEZ Y CIA'],
        [423, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GOP'],
        [424, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Graciela Elizabeth Guanes Candia'],
        [425, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GRAFICA ASUNCENA S.A.'],
        [426, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GRAN HOTEL DEL PARAGUAY S.A.'],
        [427, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GRAN PARANA S.A.'],
        [428, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GRUPO BENE S.A.'],
        [429, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GRUPO BEPA'],
        [430, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Grupo Cultural y Educativo'],
        [431, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'GRUPO INTERNACIONAL DE FINANZAS'],
        [432, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Guillermo Francisco Peroni Casal Ribeiro'],
        [433, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Gustavo Dentice Frutos'],
        [434, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Gustavo Guillermo Arrieta Maciel'],
        [435, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HABITALIS 1 S.A.'],
        [436, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Hang San Kow'],
        [437, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HANSATOUR S.R.L.'],
        [438, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Henmy Jacqueline Orue Paredes'],
        [439, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Hermann Daniel Bottger Acosta'],
        [440, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HG S.A.'],
        [441, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HIGHEST S.A.'],
        [442, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ho Jin Lee'],
        [443, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HOTEL PARANA S.A.'],
        [444, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HOTELES CONTEMPORANEO S.A.'],
        [445, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Hyun Jung Um'],
        [446, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'HZ S.R.L.'],
        [447, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Idalina Pekholtz de Turtola'],
        [448, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ignacia Evangelista Villagra de Monges'],
        [449, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ignacio Antonio Ortellado Rolon'],
        [450, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ignacio Gomez Nunes'],
        [451, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'IMPORT TELAS S.R.L.'],
        [452, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'INDERT'],
        [453, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ing. Edgar Casco'],
        [454, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ING. MIRTHA S. ACHA G.'],
        [455, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ing. Zoilo Benitez'],
        [456, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'INGENIERIA Y TECNOLOGIA S.A. (INTESA)'],
        [457, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ingrid Vanessa Kohn Sanchez'],
        [458, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'INMOBILIARIA GENERAL S.A.'],
        [459, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'INNOBRA'],
        [460, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Insp. Ppal. Lic. Gustavo Cardozo'],
        [461, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'INSTITUTO DE PREVISION SOCIAL (I.P.S.)'],
        [462, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Isabel de la Cruz Perez de Riveros'],
        [463, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ITASA S.A.'],
        [464, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'IVCA S.A.'],
        [465, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Caratulado: Jose Maria Riveros Espinoza y Mario E'],
        [466, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Felix Fabian Lopez Lovera y Dario Jose Peralta Ca'],
        [467, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Fulvia Lorena Gonzalez Correa, Pedro Juan Diaz Be'],
        [468, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Jesus Daniel Caballero Ojeda y Derlis Herrera Can'],
        [469, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Liz Paola Gonzalez Ramirez y Roberto Espinola Arr'],
        [470, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Onesima Beatriz Vaezken Garcia y Maria Celia Ibañ'],
        [471, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 10° T - Ramon Palma Casuin y Laura Giselle Quevedo Princi'],
        [472, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 3° T - Karina Fabiola Gomez Fretes y Victor Daniel Baez R'],
        [473, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 5° T - Frredy Antonio Palacios Fernandez y Nelson Gustavo'],
        [474, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'J. de Faltas 6° T - Apolonio Salvador Miño Villalba y Fernando Barrios'],
        [475, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jaime Anderson Arguello Florentin'],
        [476, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jaime Jose Bestard Duschek'],
        [477, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Javier Maria Parquet Villagra'],
        [478, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Javier Martin Palma Zelada'],
        [479, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'JCM IMPORT EXPORT S.A.'],
        [480, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'JMM ADMINISTRACION Y ASESORAMIENTO S.A.'],
        [481, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Joel Anibal Burgos Duarte'],
        [482, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jorge Adalberto Arza Maldonado'],
        [483, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jorge Anibal Caceres Franco'],
        [484, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jorge Antonio Oviedo Matto'],
        [485, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jorge Marcelino Espinola Martinez'],
        [486, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Antonio Alfonso Sosa Parquet'],
        [487, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Antonio Moreno Ruffinelli'],
        [488, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Domingo Monreale'],
        [489, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Maria Segales Romero'],
        [490, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Maria Zubizarreta Angulo'],
        [491, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Ruben Fleitas Agüero'],
        [492, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Tomas Gomez Caceres'],
        [493, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Jose Victorino Quintana Vega y Nelson Fabian Cabrera Congo '],
        [494, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'JOTOES S.A.'],
        [495, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'JOYERIA Y RELOJERIA ESPLENDOR S.R.L.'],
        [496, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Carlos Antonio Mendonca Bonnet'],
        [497, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Carlos Dionisio Mendonca Del Puerto'],
        [498, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Carlos Maria Busquets Lopez'],
        [499, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Carlos Mendieta Riveros'],
        [500, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Evangelista Aquino Pereira'],
        [501, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Jose Felix Cacavelos Benitez'],
        [502, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Leopoldo Cornet Rodas'],
        [503, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juan Pablo Fernandez Duran'],
        [504, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Julia Acosta Melgarejo'],
        [505, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Julia Graciela Lezcano de Oxilia'],
        [506, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Julio Damian Meza Huespe y Katherine Segovia de Maciel '],
        [507, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Julio Ernesto Scarone Casco'],
        [508, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Junta Municipal de Asuncion'],
        [509, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'JURADO DE ENJUICIAMIENTO DE MAGISTRADOS'],
        [510, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Justino Cesar Aquino Frutos'],
        [511, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Juvenil Hermanos Menonitas'],
        [512, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'KASBA S.A.'],
        [513, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Khalid Ali Oumeiri'],
        [514, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA CASA DEL MEDICO S.A.'],
        [515, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA CONSOLIDADA S.A. DE SEGUROS'],
        [516, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA GABINA S.A.'],
        [517, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA INDEPENDENCIA SEGUROS S.A.'],
        [518, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA LOTEADORA S.A.'],
        [519, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA PARAGUAYA INMOBILIARIA S.A.'],
        [520, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LA VIENESA S.A.'],
        [521, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LAB S.A.'],
        [522, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LABORATORIO DE ANATOMIA PATOLOGICA'],
        [523, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LABORATORIO TECNOINDUSTRIAL S.A'],
        [524, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Laura Beatriz Cabral Rodas'],
        [525, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LAZOS S.A.'],
        [526, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LEJO S.A.'],
        [527, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Geronimo Santi'],
        [528, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Graciela Marin'],
        [529, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Hugo Artemio Gonzalez'],
        [530, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Lourdes Angelica Aguilar Achar'],
        [531, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Lourdes Perez'],
        [532, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Marta Zavan'],
        [533, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Mirian Cano'],
        [534, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Mirta Cardozo'],
        [535, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Mirtha Frutos'],
        [536, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Olga Paredes'],
        [537, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Oscar G. Leguizamon'],
        [538, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Sofia Rojas'],
        [539, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lic. Veronica Koch'],
        [540, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LIDO BAR S.R.L.'],
        [541, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Liduvina Ovando de Lobo'],
        [542, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lina Mercedes Flores Riveros'],
        [543, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Liv Ljunggren Godoy'],
        [544, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Livia Cardozo'],
        [545, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Liz Caroll Cowan Benitez'],
        [546, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Liz Montserrat Caballero Gonzale'],
        [547, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LMB S.A.'],
        [548, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lourdes Andrea Baez Rodas'],
        [549, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Lucia Magdalena Laspina Galeano'],
        [550, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'LUCKY JIM'],
        [551, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Luis Alberto Pachas Medrano'],
        [552, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Luis Antonio Tomas Ayala Haedo y Blanca Acosta de Ayala'],
        [553, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Luis Osvaldo Viveros Gomez'],
        [554, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'M. Stella Palacios Otaño'],
        [555, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MAGNIFICAT ARTE'],
        [556, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Manuel Antonio Recalde Ramirez'],
        [557, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MAPFRE PARAGUAY CAMP. DE SEGUROS S.A.'],
        [558, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MAPFRE PARAGUAY S.A.'],
        [559, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Marcelo Maria Martinez Franco'],
        [560, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Marcos Antonio Yubero Aponte'],
        [561, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Marcos Juan Peroni Clifton'],
        [562, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Anna Cresencia Escher de Hiebl'],
        [563, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Antonieta Catalina Vargas Roman'],
        [564, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Asuncion Gomez sanchez de Sapriza'],
        [565, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Beatriz Leiva de Barrios'],
        [566, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Belen Cartes Berino'],
        [567, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Belen Herreros'],
        [568, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria de los Angeles Alonso de Velazquez'],
        [569, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria del Carmen Yaluk'],
        [570, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria del Rocio Masulli de Gonzalez'],
        [571, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Elizabeth Samaniego Herebia'],
        [572, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Esther Virginia Quevedo Cuenca'],
        [573, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Gabriela Riquelme Escurra'],
        [574, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Graciela Echeguren Cuevas'],
        [575, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Jose Cantero Mayeregger'],
        [576, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Laura Espinoza Gonzalez'],
        [577, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Leonor Fernandez Rodriguez'],
        [578, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Lilia Robledo Verna'],
        [579, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Lorena Segovia Azucas'],
        [580, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Luisa Hermosilla de Laspina'],
        [581, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Magdalena Gonzalez Silva'],
        [582, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Magdalena Jara de Re'],
        [583, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Marta Prieto de Gomez'],
        [584, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Natalia Torres Gimenez'],
        [585, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Rosely Kamn Ramirez'],
        [586, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Stella Peña de Vazquez'],
        [587, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maria Teresa Morales de Sosa'],
        [588, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Mariana Encarnacion Gomez Trevisan'],
        [589, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Mariana Palacios Lugo'],
        [590, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MARIANA S.A.'],
        [591, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Mariel Adelaida Balbuena Llamosas'],
        [592, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MARILIN ARMELE S.A.'],
        [593, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Marina Medina de Martinez'],
        [594, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Mario Diaz Jara'],
        [595, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Marlene Hedwing Maria Diedrich de Vogel'],
        [596, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Marta Ligia Bosio Vda. De Lopez de Filippis'],
        [597, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Martha Esperanza Armoa de Genes'],
        [598, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MASTER COLOR S.A.'],
        [599, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Matias Sebastian Recalde Roche'],
        [600, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Max Donald Eduard Pereira Gomez'],
        [601, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Maximo Wenceslao Villalba Fernandez '],
        [602, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MENEVA S.R.L.'],
        [603, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MERCADO CENTRAL S.A.'],
        [604, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Mesde Leon Osta Mendoza'],
        [605, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'META GRUPO S.R.L.'],
        [606, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Miguel Angel Martinez Gomez'],
        [607, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Miguel Arturo Vacchetta Boggino'],
        [608, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MINISTERIO DE EDUCACION Y CIENCIAS'],
        [609, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MINISTERIO DE RELACIONES EXTERIORES'],
        [610, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ministerio de Tecnologia de la Informacion y la Comunicación'],
        [611, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MINISTERIO DE TRABAJO, EMPLEO Y S.S.'],
        [612, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MINISTERIO DE URBANISMO, VIVIENDA Y HABITAT'],
        [613, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MINISTERIO DEL INTERIOR'],
        [614, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ministerio Publico'],
        [615, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MIURA S.R.L.'],
        [616, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Monica Beatriz Guirland Bareiro'],
        [617, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Monica Lucia Bernardes de Saguier'],
        [618, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MSPYBS'],
        [619, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'MUNICIPALIDAD DE FERNANDO DE LA MORA'],
        [620, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nancy Beatriz Zelaya de Gavilan'],
        [621, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nancy del Carmen Rodriguez Insfran'],
        [622, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nelson Enrique Tabacman Gonzalez'],
        [623, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nelson Ernesto Garcia Duarte'],
        [624, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nelson Vicente Martinez Nuzzarello'],
        [625, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nidia Cristina Bogado de Doldan'],
        [626, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nidia Maria Benitez Sanchez'],
        [627, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nidia Norberta Zarate de Sosa'],
        [628, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nilse Janeth Gorostiaga De Yorg'],
        [629, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nilton Adalberto Maidana Vega'],
        [630, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ninon Carina Arellano de Paredes'],
        [631, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Nora Lucia Lorenza Ruoti Cosp'],
        [632, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oficio N° 1120 Causa S/N'],
        [633, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oficio N° 228'],
        [634, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oficio N° 666 Causa S/N'],
        [635, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'OLD GERMANY S.R.L.'],
        [636, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Olegaria Gimenez de Martinez'],
        [637, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'OPTICA ARAR S.R.L.'],
        [638, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ORGANIZACIÓN DE LOS ESTADOS IBEROAMERICANOS (O.E.I.)'],
        [639, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'ORIENTE S.A.C.I.'],
        [640, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Albino Escurra Baez'],
        [641, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Bieber Alonso'],
        [642, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Daniel Gomez'],
        [643, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Paciello Samaniego'],
        [644, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Pacielo Samaniego'],
        [645, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Porfirio Garcia Medina'],
        [646, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Ramirez Acuña'],
        [647, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Oscar Ruben Rodriguez Benitez'],
        [648, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Osvaldo Armoa Acuña'],
        [649, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PAC S.A.'],
        [650, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PALACIOS PRONO & TALAVERA'],
        [651, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PALOMAR IMPORT'],
        [652, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PANADERIA LA NEGRITA S.R.L.'],
        [653, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PARAGUAY INVERSIONES S.A.'],
        [654, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Paraguay Marathon Club'],
        [655, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Pastoral Social Arquidiocesana '],
        [656, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Patrocinio Ramon Rios Ruiz'],
        [657, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Paulo Salerno Lenos y Julio Miguel Caballero Martinez '],
        [658, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Pedro Daniel Meza Zarate'],
        [659, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PEDRO FIDELIS VALIENTE SIBOL S.A.C.'],
        [660, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Pedro Ramon Ferreira Sosa'],
        [661, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PENTAGRAMA S.A.'],
        [662, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PERFILADOS PARAGUAY S.A.C.I.'],
        [663, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Perla Concepcion Gonzalez Perez'],
        [664, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Peter Poka Szabo'],
        [665, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PIRA PIRE S.A.'],
        [666, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PIRATA BAR'],
        [667, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PIZZA URBANA S.R.L.'],
        [668, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'POA RENDA S.R.L.'],
        [669, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PREMIER S.R.L.'],
        [670, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PROMEDENT S.A.'],
        [671, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PROMOCIONES E INVERSIONES MICHIGAN S.A.'],
        [672, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PROTECCION MEDICA S.A.'],
        [673, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PSI PARAGUAY S.A.'],
        [674, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'PUNTOS E HILOS DIVISION P Y H PHARMA S.R.L.'],
        [675, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'RADIO YSAPY F.M. STEREO'],
        [676, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'RAFAEL MIGLIORE COM E IND. S.R.L.'],
        [677, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Raul Alberto Olmedo Sisul'],
        [678, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'REAL CONSULADO DE DINAMARCA'],
        [679, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Reclamo del Ciudadano: Carlos Duarte'],
        [680, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'RELACIONES PUBLICAS'],
        [681, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Renata Sabrina Manon Sanchez Ozuna'],
        [682, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Resolucion N° 7842/18'],
        [683, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Resolucion N° 8076/18 Minuta N° 10908/18'],
        [684, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Resolucion N° 8224/19'],
        [685, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Resolucion N° 8516/19'],
        [686, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'RETAIL S.A.'],
        [687, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ricardo Edgar Robledo Armele'],
        [688, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Roberto Efrain Noguer Almada'],
        [689, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Roberto Jesus Brugada Huerta'],
        [690, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Rocio Gudelia Filippini Gimenez'],
        [691, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Rodolfo Antonio Berendsen Wentzensen'],
        [692, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Rodrigo Jose Maria Casco Prieto'],
        [693, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Rogelia Bogado Caceres'],
        [694, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Rogelio Barros'],
        [695, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ruben Dalmiro Baez Regunega'],
        [696, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ruben Dario Gonzalez Cantaluppi'],
        [697, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'RUMBOS S.A. DE SEGUROS'],
        [698, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Rut More Perez'],
        [699, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Ruth Martinez'],
        [700, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SABE S.A.C.'],
        [701, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SALUM WENZ'],
        [702, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SANATORIO MIGONE BATTILANA S.A.'],
        [703, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SANATORIO SAN ROQUE S.R.L.'],
        [704, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SANIDAD ANIMAL S.R.L.'],
        [705, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Sanitarios Tabacman S:R.L.'],
        [706, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Santiago Jose Maffei Franco'],
        [707, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Sara Gabriela De La Torre Berdichevsky'],
        [708, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Saturnino Cano Miranda'],
        [709, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SCG MANDATOS Y SERVICIOS S.A.'],
        [710, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SCHILLY S.A.'],
        [711, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SECRET. TECNICA DE PLANIFICACION DEL DESARROLLO ECONOMICO'],
        [712, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Secretaria de la Funcion Publica'],
        [713, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Sergio Daniel Marin Peralta'],
        [714, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SERIMAX S.R.L.'],
        [715, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SERINMSA'],
        [716, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SERVICIO FARMACEUTICO S.R.L.'],
        [717, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SERVICIOS CRESER S.A.'],
        [718, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Severiano Barreto'],
        [719, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SGS PARAGUAY S.A.'],
        [720, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Shopping Mariscal'],
        [721, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SIBOL S.A.C.'],
        [722, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SICAE S.A.'],
        [723, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Silvia Beatriz Martinez De Masi'],
        [724, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Silvia Maria Peña Masulli'],
        [725, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Simon Adalberto Cazal Fernandez'],
        [726, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SINAFOCAL'],
        [727, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SINDEC S.A.'],
        [728, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SMART CARE S.A.'],
        [729, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SOCIEDAD DANTE ALIGHIERI'],
        [730, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SOLUCIONES ECOLOGICAS'],
        [731, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Sonia Isabel Enciso Jara de Zarate'],
        [732, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Sophia Maria Barreto Conigliaro'],
        [733, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Americo Riquelme'],
        [734, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Carlos Ochipinti'],
        [735, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Enrique Gonzalez'],
        [736, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Fabio Almada Duarte'],
        [737, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Isidro Ruiz Diaz'],
        [738, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Roberto Ezequiel Godoy'],
        [739, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Tito Adrian Jara'],
        [740, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Sra. Maria Olivia Filippini de Mezgolits'],
        [741, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'STARSOFT S.R.L.'],
        [742, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Stella Mary Vergara Vda. De Acuña'],
        [743, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Stephane Laurent Jerome Duchemin Raymond'],
        [744, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Stephanie Irmgard Hoeckle Alfaro'],
        [745, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Su Yun Jeong'],
        [746, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SUDIMEX S.R.L.'],
        [747, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'SUPERMERCADO EL PAIS S.A.'],
        [748, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Susana Maria Cattaneo de Hamuy'],
        [749, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TALLER TACE'],
        [750, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Tamara Belen Brunetto Vallet'],
        [751, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Tamara Noelia Ramirez Figueredo'],
        [752, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TARTAS S.R.L.'],
        [753, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TAXARE S.A.'],
        [754, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TECNICAS Y PROYECTOS S.A.'],
        [755, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TECNO ELECTRIC S.A.'],
        [756, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TECNO VIAL S.R.L.'],
        [757, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TECNOLOGIA DE NEGOCIOS S.R.L.'],
        [758, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Teresa De Jesus Ibarrola de Gimenez'],
        [759, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Teresa Peralta Martínez'],
        [760, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TERRITORIO EMPRENDIMIENTOS S.A.'],
        [761, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'THE CCPA SCHOLL'],
        [762, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'THE CCPA SCHOOL'],
        [763, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TONINA S.A.'],
        [764, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TRANSTECNO S.A.'],
        [765, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TRAUMEDIC'],
        [766, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TRISCH S.A.'],
        [767, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TU FINANCIERA S.A.E.C.A.'],
        [768, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'TUPI RAMOS GENERALES S.A.'],
        [769, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'UNICENTRO S.A.'],
        [770, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'UNIVERSAL S.A.'],
        [771, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'UNIVERSIDAD SAN CARLOS'],
        [772, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'VALENTINA S.A.'],
        [773, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Valeria Cáceres Benítez'],
        [774, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'VALERY CONFECCIONES'],
        [775, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'VAMONOS PEST S.A.'],
        [776, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Vecinos del Barrio Pettirossi (Capitán Figari e/Rodríguez de Francia y Ana Díaz)'],
        [777, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Vecinos del Barrio Virgen de Fátima'],
        [778, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Vecinos del Lugar (Tacuarí Esq. Fulgencio Yegros)'],
        [779, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Víctor Juan Figueroa Cáceres'],
        [780, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Víctor Manuel Filartiga Cáceres'],
        [781, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Víctor Rubén Reyes Romero'],
        [782, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'VICTOR Y ASOCIADOS S.A.'],
        [783, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Victoria Insaurralde de Acuña'],
        [784, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Vilma Matilde Centurión Samaniego'],
        [785, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'VOICENTER S.A.'],
        [786, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'WAMASA S.A.'],
        [787, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'YCUA S.A.'],
        [788, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Yoko Hirai'],
        [789, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Yolanda Vergara de Ramírez'],
        [790, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'YP S.A.'],
        [791, 't', '12:00:00.000000-04', '2019-04-01 12:00', 'Zeneida Vaesken De Facetti'],
    ]

    recurr_indef = [
        [800, 't', '12:00:00.000000-04', '2019-04-07 12:00', 'INDETERMINADO'],
    ]

    for rec in range(len(recurr_indef)):
        # print(recurr_list[rec])
        Recurrente.objects.create(
            id = recurr_indef[rec][0],
            activo = recurr_indef[rec][1],
            creado = recurr_indef[rec][2],
            modificado = recurr_indef[rec][3],
            nombre = recurr_indef[rec][4],)
            # apellido = recurr_list[rec][5],
            # email = recurr_list[rec][6],
            # telefono = recurr_list[rec][7],
            # ruc = recurr_list[rec][8],
            # rmc = recurr_list[rec][9],
            