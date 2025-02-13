from django.db import models

class ThemeConfiguration(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin Profile'),
        ('farm', 'Farm Profile'),
        ('farmmanager', 'Farm Manager'),
        ('user', 'User Profile'),
    )
    role = models.CharField( max_length=20, choices=ROLE_CHOICES, unique=True,
                            help_text="User role for which this configuration applies.")
    primary_color = models.CharField( max_length=7, default='#3490dc',
                            help_text="Primary color hex code (e.g., #3490dc).")
    secondary_color = models.CharField( max_length=7, default='#ffed4a',
                            help_text="Secondary color hex code (e.g., #ffed4a).")
    background_color = models.CharField( max_length=7, default='#ffffff',
                            help_text="Background color hex code (e.g., #ffffff).")
    text_color = models.CharField( max_length=7,default='#1a202c',
                            help_text="Text color hex code (e.g., #1a202c).")

    class Meta:
        verbose_name = "Theme Configuration"
        verbose_name_plural = "Theme Configurations"

    def __str__(self):
        return f"Theme for {self.get_role_display()}"