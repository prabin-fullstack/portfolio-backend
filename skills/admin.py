from django.contrib import admin
from . models import Skill,SkillsSection,SkillGroup
# Register your models here.
admin.site.register(Skill)
admin.site.register(SkillsSection)
admin.site.register(SkillGroup)