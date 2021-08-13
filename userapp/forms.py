from userapp.models import User
from django import forms


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["can_send_sales", "can_send_updates", "can_send_new"]
        labels = {
            "can_send_sales": "We can notify you of sales",
            "can_send_updates": "We can notify you when new books are released for series you follow",
            "can_send_new": "We can notify you when new books are released"
        }
    '''new_books = forms.BooleanField(required=False, label="We can notify you when new books are released",
                                   widget=forms.CheckboxInput(attrs={"id": "new-books"}))
    follow_updates = forms.BooleanField(required=False, label="We can notify you when series you follow release new books", widget=forms.CheckboxInput(attrs={"id": "follow-updates"}))
    sales = forms.BooleanField(required=False, label="We can notify you of sales", widget=forms.CheckboxInput(attrs={"id": "sales"}))'''


class DeleteForm(forms.Form):
    pass
