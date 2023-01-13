from django.views.generic.list import ListView
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from expenses.forms import ExpenseSearchForm
from expenses.models import Expense, Category
from expenses.reports import summary_per_category, total_amount_spent


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 14

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        if self.request.GET:
            form = ExpenseSearchForm(self.request.GET)

            if form.is_valid():
                categories = form.cleaned_data.get('category')
                date_to = form.cleaned_data.get('date_to')
                date_from = form.cleaned_data.get('date_from')
                queryset = Expense.objects.all()

                if date_to and date_from:
                    queryset = queryset.select_related('category').filter(date__gte=date_to,
                                                                          date__lte=date_from).filter(
                        category__in=categories)
                elif date_to:
                    queryset = queryset.select_related('category').filter(date__lte=date_to).filter(
                        category__in=categories)
                elif date_from:
                    queryset = queryset.select_related('category').filter(date__lte=date_from).filter(
                        category__in=categories)
                else:
                    queryset = queryset.select_related('category').filter(category__in=categories)

        else:
            form = ExpenseSearchForm()

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset), **kwargs,
            total_amount_spent=total_amount_spent(self.object_list),
            amount_category=self.object_list.all().select_related('category').values('category__name').annotate(
                Sum('amount')),
            summary_per_month=self.object_list.annotate(month=TruncMonth("date")).values('month').annotate(
                sum=Sum("amount")),
            summary_per_year=self.object_list.annotate(year=TruncYear("date")).values('year').annotate(
                sum=Sum("amount")),

        )


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

