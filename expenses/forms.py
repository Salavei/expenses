from django import forms
import datetime
from expenses.models import Category, Expense


class ExpenseSearchForm(forms.Form):
    range_year = Expense.objects.all().order_by('date').first().date.year

    date_to = forms.DateField(widget=forms.SelectDateWidget(years=range(range_year, datetime.date.today().year)),
                              required=False)
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=range(range_year, datetime.date.today().year)),
                                required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              required=False, widget=forms.SelectMultiple)

    class Meta:
        fields = ('category', 'date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
