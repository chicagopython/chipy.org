from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from flatblocks.admin import FlatBlockAdmin
from flatblocks.models import FlatBlock
from ckeditor.widgets import CKEditorWidget


class CustomFlatpageForm(FlatpageForm):
    def __init__(self, *args, **kwargs):
        super(CustomFlatpageForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget = CKEditorWidget()


class CustomFlatPageAdmin(FlatPageAdmin):
    form = CustomFlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)


class CustomFlatBlockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomFlatBlockForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget = CKEditorWidget()


class CustomFlatBlockAdmin(FlatBlockAdmin):
    form = CustomFlatBlockForm


admin.site.unregister(FlatBlock)
admin.site.register(FlatBlock, CustomFlatBlockAdmin)
