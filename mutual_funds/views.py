from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from mutual_funds.forms import InvestmentForm
from mutual_funds.models import investment
from mutual_funds.static_method import get_data


class investmentView(View):
    form_class = InvestmentForm
    initial = {'key': 'value'}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        objects = investment.objects.all()
        mf_data = get_data()
        for obj in objects:
            amount = float(mf_data[obj.mutual_fund_name]) * float(obj.units)
            obj.amount = round(amount, 2)
            obj.back_color = 'greenyellow' if amount > obj.investment_amount else 'orangered'
        return render(request, self.template_name, {'form': form, 'objects': objects, 'mf_data': mf_data})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        objects = investment.objects.all()
        if form.is_valid():
            form.save()
            return redirect('mutual_funds_app:investment')
        return render(request, self.template_name, {'form': form, 'objects': objects})


def withdrawView(request, id):
    date = datetime.today()
    mf_data = get_data()
    obj = investment.objects.get(pk=id)
    withdraw_amount = float(mf_data[obj.mutual_fund_name]) * float(obj.units)
    investment.objects.filter(pk=id).update(withdraw_amount=round(withdraw_amount, 2), withdraw_date=date.strftime('%Y-%m-%d'))
    return redirect('mutual_funds_app:investment')



