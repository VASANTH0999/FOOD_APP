from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        labels = {
            'rating': 'Rate Your Experience',
            'comments': 'Feedback Comments',
        }
        help_texts = {
            'rating': 'Choose a rating from 1 (Poor) to 5 (Excellent)',
        }
        widgets = {
            'rating': forms.Select(choices=[
                (5, '5 - Excellent'),
                (4, '4 - Very Good'),
                (3, '3 - Good'),
                (2, '2 - Fair'),
                (1, '1 - Poor')
            ]),
            'comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your feedback'}),
        }

    def clean_comments(self):
        comments = self.cleaned_data.get('comments')
        if len(comments) < 10:
            raise forms.ValidationError('Feedback must be at least 10 characters long.')
        return comments
