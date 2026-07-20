from django.contrib import admin
from .models import Beat, BeatCategory, Testimonial,Purchase

admin.site.register(Beat)
admin.site.register(BeatCategory)
admin.site.register(Testimonial)
admin.site.register(Purchase)