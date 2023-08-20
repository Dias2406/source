from django.shortcuts import render, redirect, get_object_or_404
from student.models import Module, ModuleInfo, Cognitive, Behavioural
from student.forms import AffectiveForm
from student.utils import setColor
from account.models import Account
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages

# Create your views here.



def cognitive_view(request,slug):
	if not request.user.is_authenticated:
		return (redirect("login"))
	
	context = {}

	module = get_object_or_404(Module, slug = slug)
	modules_info = ModuleInfo.objects.filter(student = request.user)
	module_info = modules_info.filter(module = module).first()
	context['module'] = module
	context['modules_info'] = modules_info
	context['module_info'] = module_info

	cognitive_info = Cognitive.objects.filter(student = request.user).filter(module = module).first()
	context['cognitive_coursework'] = cognitive_info.coursework
	context['cognitive_exam'] = cognitive_info.exam

	context["average"] = cognitive_info.overall

	context['color_coursework'] = setColor(cognitive_info.coursework)
	context['color_exam'] = setColor(cognitive_info.exam)
	context['color_average'] = setColor(cognitive_info.overall)
	

	return render(request, "engagement/cognitive.html", context)

def behavioural_view(request, slug):
	if not request.user.is_authenticated:
		return (redirect("login"))
	
	context = {}
	context["week"] = {}
	module = get_object_or_404(Module, slug = slug)
	modules_info = ModuleInfo.objects.filter(student = request.user)

	attendance = 0
	behaviourals = Behavioural.objects.filter(student = request.user).filter(module = module)

	# calculating average attendance
	for behavioural in behaviourals:
		attendance += behavioural.attendance
	try:
		avrg_attendance = float(attendance / len(behaviourals))
		temp = 100 - avrg_attendance
	except:
		avrg_attendance = 0
		temp=0

	# storing attendance at the specific week
	number_of_weeks = len(behaviourals)
	for i in range(1, number_of_weeks + 1):
		for behavioural in behaviourals:
			if behavioural.week == i:
				context["week"][i] = behavioural.attendance


	context['module'] = module
	context['modules_info'] = modules_info
	context['attendance'] = round(avrg_attendance,2)
	context["val"] = round(temp,2)
	return render(request, 'engagement/behavioural.html', context)

def affective_view(request, slug):
	if not request.user.is_authenticated:
		return (redirect("login"))
	
	context = {}

	module = get_object_or_404(Module, slug = slug)
	modules_info = ModuleInfo.objects.filter(student = request.user)
	module_info = modules_info.filter(module = module).first()
	context['module'] = module
	context['modules_info'] = modules_info
	context['module_info'] = module_info

	if 'submit' in request.POST:
		form = AffectiveForm(request.POST)
		if form.is_valid():
			# check the student last answer date to see if it was recently answered 
			try:
				elapesed_time = timezone.now() - module_info.answer_date
				cooldown = timedelta(days=7)
			except:
				cooldown = 0
				elapesed_time = 1
			# check if the cooldown period is over
			if elapesed_time > cooldown:
				obj = form.save(commit=False)
				student = Account.objects.filter(email=request.user.email).first()
				obj.student = student
				obj.module = module
				obj.week = str(module_info.week)
				# update the Module Information object
				module_info.week += 1
				module_info.answer_date = datetime.now()
				module_info.save()
				obj.save()
				form = AffectiveForm()
				messages.success(request, 'Thank you for your answer!')
			else:
				temp = cooldown - elapesed_time

				messages.error(request, 'Sorry, you can only reflect once in a week - '+ str(temp) +' left')
	else:
		form = AffectiveForm() 


	context['form'] = form

	
	return render(request, "engagement/affective.html", context)