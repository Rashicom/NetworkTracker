from django.forms import forms

class SystemUsageForm(forms.Form):
    process_name = forms.CharField(required=True)
    memory_percent = forms.FloatField(required=True)
    memory_usage = forms.FloatField(required=False)


class SystemInfoForm(forms.Form):
    username = forms.CharField()
    system_info = SystemUsageForm()

