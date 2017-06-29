from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Aparcamiento,PaginaUsuario,Comentario,AparcamientoSeleccionado
from django.contrib.auth.models import User
from parser_xml import getParking
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.template import RequestContext
from django.db.models import Count

# Create your views here.
@csrf_exempt
def Principal(request):
	aparcs = Aparcamiento.objects.all()
    #COMPRUEBA SI SE HA PARSEADO EL XML => LO PARSEA
	if not aparcs:
		aparcs = getParking()
		for aparca in aparcs:
			try:
				nuevo_aparca = Aparcamiento(nombre = aparca["NOMBRE"],
				descripcion = aparca["DESCRIPCION"], accessibilidad= aparca["ACCESIBILIDAD"],
				url = aparca["CONTENT-URL"], barrio = aparca["BARRIO"],
				distrito = aparca["DISTRITO"], latitud = aparca["LATITUD"],
				longitud = aparca["LONGITUD"],telefono = aparca["TELEFONO"], email = aparca["EMAIL"])
			except KeyError:
				try:
					nuevo_aparca = Aparcamiento(nombre = aparca["NOMBRE"],
					descripcion = aparca["DESCRIPCION"], accessibilidad= aparca["ACCESIBILIDAD"],
					url = aparca["CONTENT-URL"], barrio = aparca["BARRIO"],
					distrito = aparca["DISTRITO"], latitud = aparca["LATITUD"], 
					longitud = aparca["LONGITUD"])
				except KeyError:
					try:
						nuevo_aparca = Aparcamiento(nombre = aparca["NOMBRE"],
						descripcion = aparca["DESCRIPCION"], accessibilidad= aparca["ACCESIBILIDAD"],
						url = aparca["CONTENT-URL"], barrio = aparca["BARRIO"],
						distrito = aparca["DISTRITO"])
					except KeyError:
						try:
							nuevo_aparca = Aparcamiento(nombre = aparca["NOMBRE"],
							descripcion = aparca["DESCRIPCION"], accessibilidad= aparca["ACCESIBILIDAD"],
							url = aparca["CONTENT-URL"])
						except KeyError:
							continue
			nuevo_aparca.save()
	lista_aparcamientos = []
	aparcamientos_populares = Aparcamiento.objects.annotate(quantity=Count('cuantidad_likes')).order_by('-cuantidad_likes')
	if aparcamientos_populares[0].quantity>0:
		for contador in range(5):
			if aparcamientos_populares[contador].quantity>0:
				aparcamiento = Aparcamiento.objects.get(nombre = aparcamientos_populares[contador])
				lista_aparcamientos += {aparcamiento}
	lista_usuarios=[]
	usuarios = User.objects.all()
	if usuarios:
		for usuario in usuarios:
			lista_usuarios.append(usuario)
			
	template = get_template('principal.html')
	context = RequestContext(request, {'lista_aparcamientos' : lista_aparcamientos,'lista_usuarios':lista_usuarios})		
	return HttpResponse(template.render(context))


@csrf_exempt
def Aparcamientos(request):
	if request.method == 'GET':
		lista_aparcamientos = Aparcamiento.objects.all()
	else:
		dis = str(request.body).split("=")[1][:-1]
		if dis != "None":
			lista_aparcamientos = Aparcamiento.objects.filter(distrito=dis)
	template = get_template('aparcamientos.html')
	context = RequestContext(request, {'lista_aparcamientos' : lista_aparcamientos})
	return HttpResponse(template.render(context))

@csrf_exempt
def Aparcamientos_id(request,index):
	aparc = Aparcamiento.objects.get(id = index)
	if request.method == "POST":
		user = request.user.username
		user_reg = User.objects.get(username = user)	
		recurso = request.POST.get('recurso')
		contenido = str(request.body)[2:].split('=')[1][:-1]		
		if recurso == '1':#comentario
			nuevo_comentario = Comentario(anotacion=contenido,aparcamiento=aparc,usuario=user_reg)
			nuevo_comentario.save()
		elif recurso == '2':#like
			lk = aparc.cuantidad_likes
			lk = lk+1
			aparc.cuantidad_likes = lk
			aparc.save()
		elif recurso == '3':#fav
			nuevo_favorito= AparcamientoSeleccionado(aparcamiento= aparc ,usuario= user_reg)
			print("***")
			print(nuevo_favorito.aparcamiento)
			nuevo_favorito.save()
				
	template = get_template('aparcamiento.html')
	context = RequestContext(request, {'aparcamiento' : aparc,'id':str(index)})
	return HttpResponse(template.render(context))

@csrf_exempt
def auth(request):
	if request.method == "POST":
		username = strip_tags(request.POST.get('usuario_login'))
		password = request.POST.get('contra_login')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		return HttpResponseRedirect('/')
	else:
		return HttpResponse("No esta registrado")

@csrf_exempt
def PaginaUsuario(request,usuario):
	user_reg = User.objects.get(username = usuario)
	lista_usuarios_fav = AparcamientoSeleccionado.objects.filter(usuario=user_reg)
	if request.method =="GET":
		title = "Pagina de "+usuario
	else:#me llega un POST
		title=request.POST.get('titulo')
		tamanho = request.POST.get('tamanho')
		print(title)
		print(str(tamanho))
		guardar_estilo = PaginaUsuario(usuario = user_reg,titulo=title,tamanho=tamanho)
		guardar_estilo.save()
	template = get_template('paginausuario.html')
	context = RequestContext(request, {'titulo':title,'lista_usuarios_fav':lista_usuarios_fav,'usuario':usuario})
	return HttpResponse(template.render(context))

def About(request):
	template = get_template('about.html')
	return HttpResponse(template.render(''))
