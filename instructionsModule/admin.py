from django.contrib import admin
from .models import InstructionList, Instruction,InstructionAttachment, Note

admin.site.register(InstructionList)
admin.site.register(Instruction)
admin.site.register(InstructionAttachment)
admin.site.register(Note)
