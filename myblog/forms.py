from django import forms


class MessageForm(forms.Form):
    username = forms.CharField(label='名字', max_length=30, required=True)
    content = forms.CharField(
        label='留言', max_length=150,
        widget=forms.Textarea(attrs={'cols': '56', 'rows': '5'}),
        required=True
    )



