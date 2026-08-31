from django.contrib import admin
from .models import Medicine  # Aapka Medicine Model

# Admin Panel Site Names
admin.site.site_header = "National Pharma"
admin.site.site_title = "National Pharma"
admin.site.index_title = "National Pharma"

# Medicine Model ko register karein (Is line se +Add button wapas aayega)
admin.site.register(Medicine)