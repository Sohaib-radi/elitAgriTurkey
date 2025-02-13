from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType   
from django.contrib.contenttypes.fields import GenericForeignKey   
 

class CustomFieldQuerySet(models.QuerySet):
    def custom_filter(self, **kwargs): return self.filter(**kwargs)   

class CustomFieldManager(models.Manager):
    def get_queryset(self): return CustomFieldQuerySet(self.model, using=self._db)
    def custom_filter(self, **kwargs): return self.get_queryset().custom_filter(**kwargs)
 

 
class InstructionList(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("List Name"), help_text=_("Name of the instruction list"))   
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description of the list"))   
    image = models.ImageField(upload_to='instruction_lists/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an image for the list"))  # إرفاق صورة
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the list was created"))  # تاريخ الإنشاء

    objects = CustomFieldManager()   

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Instruction List")  
        verbose_name_plural = _("Instruction Lists")   
        ordering = ['name']  

 
class Instruction(models.Model):
    instruction_list = models.ForeignKey(InstructionList, on_delete=models.CASCADE, related_name='instructions', verbose_name=_("Instruction List"), help_text=_("Associated instruction list"))   
    name = models.CharField(max_length=255, verbose_name=_("Instruction Name"), help_text=_("Name of the instruction"))  
    goal = models.CharField(max_length=255, verbose_name=_("Goal"), help_text=_("Goal of the instruction")) 
    description = models.TextField(verbose_name=_("Description"), help_text=_("Instruction description"))  
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date for the instruction"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the instruction was created"))  

    objects = CustomFieldManager()   

    def __str__(self): return f"{self.name} ({self.instruction_list.name})"
    class Meta:
        verbose_name = _("Instruction")  
        verbose_name_plural = _("Instructions")   
        ordering = ['-date']   

 
class InstructionAttachment(models.Model):
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, related_name='attachments', verbose_name=_("Instruction"), help_text=_("Associated instruction"))   
    attachment = models.FileField(upload_to='instruction_attachments/', verbose_name=_("Attachment"), help_text=_("Attach a video, image, or note"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Attachment description"))  
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date for the attachment"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the attachment was added"))  

    objects = CustomFieldManager()  

    def __str__(self): return f"Attachment for {self.instruction.name}"
    class Meta:
        verbose_name = _("Instruction Attachment")  
        verbose_name_plural = _("Instruction Attachments")   
        ordering = ['-date']   

 
 
class Note(models.Model):
    note_number = models.CharField(max_length=50, unique=True, verbose_name=_("Note Number"), help_text=_("Unique note number"))  
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"), help_text=_("Type of the related entity"))  
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"), help_text=_("ID of the related entity"))  
    content_object = GenericForeignKey('content_type', 'object_id')   
    description = models.TextField(verbose_name=_("Description"), help_text=_("Note description"))  
    current_date = models.DateField(verbose_name=_("Current Date"), help_text=_("Current date"))  
    target_date = models.DateField(verbose_name=_("Target Date"), help_text=_("Target date for reminder"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the note was created"))   

    objects = CustomFieldManager()  

    def __str__(self): return f"Note {self.note_number}"
    class Meta:
        verbose_name = _("Note")  
        verbose_name_plural = _("Notes")   
        ordering = ['-created_at']   
