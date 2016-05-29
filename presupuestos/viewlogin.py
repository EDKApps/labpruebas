# -- coding: utf-8 --
#ver https://docs.djangoproject.com/es/1.9/topics/auth/default/
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import Context

@csrf_exempt #solo en esta vista desactivar el control de Crsf
def user_login(request):
	#Si el request es HTTP POST, intentar extraer la información relevante
	if request.method == 'POST':
		#reunir el usuario y clave provisto por el usuario
		#Se obtiene del form Login.
		username = request.POST.get('username')
		password = request.POST.get('password')
		#consultar a django si la combinación usuario-clave es válida
		#si es válida se retorna un objeto User
		user = authenticate(username=username, password=password)

		#Si no existe el objeto--> no se encontró el usuario con las credenciales indicadas
		if user:
			if user.is_active:
				#Si el usuario es válido y activo, podemos loguearlo
				login(request,user)
				return HttpResponseRedirect( reverse('presupuestos:presupuesto_listar') )
			else:
				context = Context({"mensaje": "Su cuenta se encuentra desactivada"})
				return render(request, 'presupuestos/login.html', context)
		else:
			context = Context({"mensaje": "Ha indicado datos de acceso inválidos"})
			return render(request, 'presupuestos/login.html', context)
	else: #Si no es POST, asumo GET y muestro el formulario de Login
		#No paso variables de contexto, así que va el diccionario vacio
		return render(request, 'presupuestos/login.html',{})

# Use the login_required() decorator to ensure only those logged in can access the view.
#@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    print request.session
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('presupuestos:login') )
