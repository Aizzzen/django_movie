from django import forms

from movies.models import Reviews


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("email", "name", "text", )
