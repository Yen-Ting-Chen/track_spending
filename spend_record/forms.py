from django import forms
from .models import Record, Category
from datetime import date
from django.contrib.auth.forms import AuthenticationForm
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['date', 'record_type', 'category', 'name', 'amount','payment_method']
        labels = {
            'date': '日期',
            'record_type': '類型',
            'category': '分類',
            'payment_method': '消費方式',
            'name': '名稱',
            'amount': '金額',
            
        }
        today_str = date.today().strftime('%Y-%m-%d')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date','value': today_str},format='%Y-%m-%d'),
            # 'note': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        } 
        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',       # ✅ 套用 Bootstrap 樣式
            'placeholder': '輸入帳號'      # ✅ 加入 placeholder
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '輸入密碼'
        })
    )
