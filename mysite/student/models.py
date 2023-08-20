from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from teacher.models import Teacher

class Module(models.Model):
	code            = models.CharField(verbose_name="Module Code", max_length=30, unique=True)
	name            = models.CharField(verbose_name="Name", max_length=50)
	teacher 		= models.ForeignKey(Teacher, on_delete=models.CASCADE)
	ca_weight       = models.DecimalField(max_digits=2,decimal_places=1, default=0)
	exam_weight     = models.DecimalField(max_digits=2,decimal_places=1, default=0)
	slug 			= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.code
	

def pre_save_module_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.code)

pre_save.connect(pre_save_module_post_receiver, sender=Module)


class ModuleInfo(models.Model):
	module              = models.ForeignKey(Module, on_delete=models.CASCADE)
	student             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	week            	= models.IntegerField(default=0)
	answer_date         = models.DateTimeField(blank=True, null=True)


	def __str__(self):
		return self.module.code + "-" + " " + self.student.first_name + " " + self.student.last_name
	
class Behavioural(models.Model):
	week				= models.IntegerField(verbose_name = "Week", default=None)
	module              = models.ForeignKey(Module, on_delete=models.CASCADE)
	student             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	attendance          = models.DecimalField(max_digits=6,decimal_places=2, default=0)

	def __str__(self):
		return "Week: " + str(self.week) + ", " + self.module.code + " " + self.student.username
	
class Affective(models.Model):
	auto_increment_id   = models.AutoField(primary_key=True)
	week            	= models.IntegerField(default=0)
	student             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	module              = models.ForeignKey(Module, on_delete=models.CASCADE)
	emoji               = models.CharField(verbose_name="Emoji", max_length=30, )
	text				= models.CharField(verbose_name="Explanation", max_length=50, default = "")

	def __str__(self):
		return "Week: " + str(self.week) + ", " + self.module.code + " " + self.student.username + " " + self.emoji
	
class Cognitive(models.Model):
	auto_increment_id   = models.AutoField(primary_key=True)
	module              = models.ForeignKey(Module, on_delete=models.CASCADE)
	student             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	coursework          = models.DecimalField(max_digits=5,decimal_places=2, default=0)
	exam                = models.DecimalField(max_digits=5,decimal_places=2, default=0)
	overall             = models.DecimalField(max_digits=5,decimal_places=2, default=0)

	def save(self, *args, **kwargs):
		self.overall = (self.coursework * self.module.ca_weight) + (self.exam * self.module.exam_weight)
		super(Cognitive, self).save(*args, **kwargs)





	def __str__(self):
		return self.module.code + "-" + " " + self.student.first_name + " " + self.student.last_name