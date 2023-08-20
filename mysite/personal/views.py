from django.shortcuts import render, redirect
from student.models import Module, ModuleInfo, Cognitive, Behavioural, Affective
from teacher.models import Teacher
from account.models import Account
from student.utils import setColor
from collections import Counter

# Create your views here.

def home_screen_view(request):
	context = {}

	if not request.user.is_authenticated :
		return redirect("login") 
	
	# check if user student or teacher
	if not request.user.is_teacher:
		modules = ModuleInfo.objects.filter(student = request.user)
		context['modules'] = modules

		sum_attendance = 0

		sum_coursework = 0
		sum_exam = 0
		sum_final = 0

		# iteration through modules
		for module in modules:
			attendance = 0
			behaviourals = Behavioural.objects.filter(module=module.module).filter(student = request.user)
			# sum attendance across all modules
			for behavioural in behaviourals:
				attendance += behavioural.attendance
			avrg_attendance = attendance / len(behaviourals)
			sum_attendance += avrg_attendance
			
			# sum assessment marks
			cognitive = Cognitive.objects.filter(module = module.module).filter(student = request.user).first()
			sum_coursework += cognitive.coursework
			sum_exam += cognitive.exam
			sum_final += cognitive.overall

		
		#average attendance across all modules
		temp = 100 - sum_attendance / len(modules)
		context['avrg_attendance'] = round(float(sum_attendance / len(modules)),2)
		context['temp'] = round(float(temp),2)
		# average assessments marks across all modules
		avrg_coursework = sum_coursework / len(modules)
		avrg_exam = sum_exam / len(modules)
		avrg_final = sum_final / len(modules)
		context['avrg_exam'] = avrg_exam
		context['avrg_coursework'] = avrg_coursework
		context['avrg_overall'] = avrg_final
		context['exam_color'] = setColor(avrg_exam)
		context['ca_color'] = setColor(avrg_coursework)
		context['overall_color'] = setColor(avrg_final)
	else:
		teacher = Teacher.objects.filter(account = request.user).first()
		modules = Module.objects.filter(teacher = teacher)

		context["teacher"] = teacher
		context["modules"] = modules

		# dictionaries for behavioural sata
		context["week_attendance"] = {}
		context["avrg_week_attendance"] = {}
		context["avrg_week_attendance"]["week"] = {
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
		# dictionaries for cognitive data
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
		# affective dictionary for storing emojis of each week
		affectives = Affective.objects.all()
		number_of_weeks = max(affective.week for affective in affectives)
		context["affectives_week"] = {}
		for i in range(1, number_of_weeks+1):
			context["affectives_week"][str(i)] = []


		behaviourals = Behavioural.objects.all()
		sum_week_attendance = 0
		avrg_attendance = 0
		# calculate overall average attendance across modules
		for module in modules:
			sum_attendance = 0
			behaviourals = Behavioural.objects.filter(module = module)
			for behavioural in behaviourals:
				sum_attendance += behavioural.attendance
		
			avrg_attendance += (sum_attendance / len(behaviourals))
		
		avrg_attendance = avrg_attendance / len(modules)
		temp = 100 - round(avrg_attendance, 2)

		context["avrg_attendance"] = round(avrg_attendance, 2)
		context["val"] = temp

		context['cognitive_coursework'] = 0
		context['cognitive_exam'] = 0
		context['cognitive_overall'] = 0

		# iteration through modules
		for module in modules:
			sum_ca = 0
			sum_exam = 0
			sum_overall = 0
			context[module.code] = {}
			behaviourals = Behavioural.objects.filter(module = module)
			number_of_students = len(ModuleInfo.objects.filter(module = module))
			number_of_weeks = (len(behaviourals) / number_of_students)
			# sum attendance of each week 
			# iteration through weeks
			for i in range(1, int(number_of_weeks) + 1):
				context["week_attendance"][i] = 0
				for behavioural in behaviourals:
					if behavioural.week == i:
						sum_week_attendance += behavioural.attendance
					avrg_week_attendance = sum_week_attendance / number_of_students
				context["week_attendance"][i] += float(avrg_week_attendance)
				sum_week_attendance = 0
				context["avrg_week_attendance"]["week"][str(i)] += context["week_attendance"][i]
			
			cognitives = Cognitive.objects.filter(module = module)
			# sum assessment marks across modules
			for cognitive in cognitives:
				sum_ca += cognitive.coursework
				sum_exam += cognitive.exam
				sum_overall += cognitive.overall
			
			context['cognitive_coursework'] += (sum_ca / number_of_students)
			context['cognitive_exam'] += (sum_exam / number_of_students)
			context['cognitive_overall'] += (sum_overall / number_of_students)

			affectives = Affective.objects.filter(module = module)
			number_of_weeks = max(affective.week for affective in affectives)
			# storing list of emojis in a specific week
			for i in range(1,number_of_weeks+1):
				for affective in affectives:
					if affective.week == i:
						context["affectives_week"][str(i)].append(affective.emoji)
						
		# average assessment marks across modules
		context['cognitive_coursework'] = round(float(context['cognitive_coursework'] / len(modules)),2)
		context['cognitive_exam'] = round(float(context['cognitive_exam'] / len(modules)),2)
		context['cognitive_overall'] = round(float(context['cognitive_overall'] / len(modules)),2)
		context['color_coursework'] = setColor(context['cognitive_coursework'])
		context['color_exam'] = setColor(context['cognitive_exam'])
		context['color_overall'] = setColor(context['cognitive_overall'])			

		# storing most frequently used emojis of each week
		number_of_weeks = len(context["affectives_week"])
		for i in range(1, number_of_weeks + 1):
			counter = (Counter(context["affectives_week"][str(i)]))
			context["affectives_week"][str(i)] = []
			temp = counter.most_common(1)[0][1]
			for k,v in counter.items():
				if v >= temp:
					context["affectives_week"][str(i)].append(k)
					temp = v

		context["values"] = context["affectives_week"].values()

		# average attendance of each week across modules
		number_of_weeks = len(context["avrg_week_attendance"]["week"])
		for i in range(1, number_of_weeks + 1):
			context["avrg_week_attendance"]["week"][str(i)] = round(float(context["avrg_week_attendance"]["week"][str(i)] / len(modules)),2)
		

	return render(request, "personal/home.html", context)
