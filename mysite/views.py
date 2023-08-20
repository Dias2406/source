from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from engagement.models import Module, ModuleInfo, Cognitive, Behavioural, Affective
from tracking.models import Teacher
from tracking.utils import setCaRange, setExamRange, setOverallRange, setHonours
from engagement.utils import setColor
from account.models import Account
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from collections import Counter

# Create your views here.

def behavioural_view(request, slug):
	if not request.user.is_authenticated:
		return (redirect("login"))
	
	if not request.user.is_teacher:
		return (redirect("login"))
	
	context = {}

	teacher = Teacher.objects.filter(account = request.user).first()

	modules = Module.objects.filter(teacher = teacher)
	module = get_object_or_404(Module, slug = slug)
	behaviourals = Behavioural.objects.filter(module = module)
	module_infos = ModuleInfo.objects.filter(module = module)

	context["modules"] = modules
	context["module"] = module

	attendance = 0

	for behavioural in behaviourals:
		attendance += behavioural.attendance
	avrg_attendance = attendance / len(behaviourals)
	temp = 100 - round(avrg_attendance,2)

	context["attendance"] = round(avrg_attendance,2)
	context["val"] = temp
	
	week_attendance = 0
	context["week"] = {}
	number_of_weeks = len(behaviourals) / len(module_infos)

	for i in range(1, int(number_of_weeks) + 1):
		for behavioural in behaviourals:
			if behavioural.week == i:
				week_attendance += behavioural.attendance
			context["week"][i] = round(float(week_attendance / len(module_infos)),2)
		week_attendance = 0


	
	context["student"] = {}

	for module_info in module_infos:
		student_attendance = 0
		context["student"][module_info.student] = {
		"username": "",
		"first_name": "",
		"last_name": "",
		"attendance": 0
		}
		context["student"][module_info.student]["week"] = {
			"1": 0,
			"2": 0,
			"3": 0,
			"4": 0,
			"5": 0,
			"6": 0,
			"7": 0,
			"8": 0,
			"9": 0,
			"10": 0,
			"11": 0,
			"12": 0
		}
		student_attendance_infos = Behavioural.objects.filter(module = module_info.module).filter(student = module_info.student)
		for student_attendance_info in student_attendance_infos:
			student_attendance += student_attendance_info.attendance
		avrg_student_attendance = float(student_attendance / len(student_attendance_infos))
		context["student"][module_info.student]["username"] = module_info.student.username
		context["student"][module_info.student]["first_name"] = module_info.student.first_name
		context["student"][module_info.student]["last_name"] = module_info.student.last_name
		context["student"][module_info.student]["attendance"] = round(avrg_student_attendance,2)

		for i in range(1, len(student_attendance_infos)+1):
			for student_attendance_info in student_attendance_infos:
				if student_attendance_info.week == i:
					context["student"][module_info.student]["week"][str(i)] = float(student_attendance_info.attendance)


	context["student_infos"] = context["student"].values()

	return render(request, "tracking/behavioural.html", context)

def cognitive_view(request,slug):
	if not request.user.is_authenticated:
		return (redirect("login"))

	if not request.user.is_teacher:
		return (redirect("login"))

	context = {}
	context["exam_mark"] = {
		"100": 0,
		"89": 0,
		"79": 0,
		"69": 0,
		"59": 0,
		"49": 0,
		"40": 0,
	}

	context["ca_mark"] = {
		"100": 0,
		"89": 0,
		"79": 0,
		"69": 0,
		"59": 0,
		"49": 0,
		"40": 0,
	}


	context["overall_mark"] = {
		"100": 0,
		"89": 0,
		"79": 0,
		"69": 0,
		"59": 0,
		"49": 0,
		"40": 0,
	}
	
	teacher = Teacher.objects.filter(account = request.user).first()

	modules = Module.objects.filter(teacher = teacher)
	module = get_object_or_404(Module, slug = slug)

	cognitives = Cognitive.objects.filter(module = module)
	context["cognitive"] = {}
	for cognitive in cognitives:
			context["cognitive"][cognitive.student] = {
				"username": "",
				"first_name": "",
				"last_name": "",
				"coursework": 0,
				"exam": 0,
				"overall": 0,
				"honours": "",
				"honours_colour": "" 
			}
			ca_mark = cognitive.coursework
			exam_mark = cognitive.exam
			overall = cognitive.overall

			setCaRange(context, ca_mark)
			setExamRange(context, exam_mark)
			setOverallRange(context, overall)

			context["cognitive"][cognitive.student]["username"] = cognitive.student.username
			context["cognitive"][cognitive.student]["first_name"] = cognitive.student.first_name
			context["cognitive"][cognitive.student]["last_name"] = cognitive.student.last_name
			context["cognitive"][cognitive.student]["coursework"] = cognitive.coursework
			context["cognitive"][cognitive.student]["exam"] = cognitive.exam
			context["cognitive"][cognitive.student]["overall"] = cognitive.overall
			context["cognitive"][cognitive.student]["honours"] = setHonours(cognitive.overall)
			context["cognitive"][cognitive.student]["honours_colour"] = setColor(cognitive.overall)


	context["cognitives"] = context["cognitive"].values()
	context["modules"] = modules
	context["module"] = module
	return render(request, "tracking/cognitive.html", context)

def affective_view(request, slug):
	if not request.user.is_authenticated:
		return (redirect("login"))
	
	if not request.user.is_teacher:
		return (redirect("login"))
	
	context = {}
	context["week"] = {}

	
	teacher = Teacher.objects.filter(account = request.user).first()
	modules = Module.objects.filter(teacher = teacher)
	module = get_object_or_404(Module, slug = slug)
	context["modules"] = modules
	context["module"] = module

	module_infos = ModuleInfo.objects.filter(module = module)

	affectives = Affective.objects.filter(module = module)
	number_of_weeks = max(affective.week for affective in affectives)
	for i in range(1, number_of_weeks):
		context["week"][i] = []
		for affective in affectives:
			if affective.week == i:
				context["week"][i].append(affective)

	context["emoji"] = {}
	for affective in affectives:
		if affective.emoji not in context["emoji"].keys():
			context["emoji"][affective.emoji] = []
	
	for key in context["emoji"].keys():
		for affective in affectives:
			if affective.emoji == key:
				context["emoji"][affective.emoji].append(affective.text)
	context["emojis"] = context["emoji"]
	context["affective_weeks"] = context["week"].values()
	context["module_infos"] = module_infos
	context["affectives"] = affectives
	return render(request, "tracking/affective.html", context)