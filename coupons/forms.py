from django import forms

from shop_app.models import UserProfile


class CouponeApplyForm(forms.Form):
    coupon_code = forms.CharField(label='')


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['picture', 'quote', 'location']


