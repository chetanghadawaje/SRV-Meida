from datetime import datetime, timedelta
from django import forms
from mutual_funds.models import investment
from mutual_funds.static_method import get_data
from django.core.exceptions import ValidationError


class InvestmentForm(forms.ModelForm):
    MUTUAL_FUND = (('Axis Overnight Fund - Direct Plan - Daily Dividend Option', 'Axis Overnight Fund - Direct Plan - Daily Dividend Option'), ('Axis Overnight Fund - Direct Plan - Growth Option', 'Axis Overnight Fund - Direct Plan - Growth Option'), ('Axis Overnight Fund - Direct Plan - Monthly Dividend Option', 'Axis Overnight Fund - Direct Plan - Monthly Dividend Option'), ('Axis Overnight Fund - Direct Plan - Weekly Dividend Option', 'Axis Overnight Fund - Direct Plan - Weekly Dividend Option'), ('Axis Overnight Fund - Regular Plan - Daily Dividend Option', 'Axis Overnight Fund - Regular Plan - Daily Dividend Option'), ('Axis Overnight Fund - Regular Plan - Growth Option', 'Axis Overnight Fund - Regular Plan - Growth Option'), ('Axis Overnight Fund - Regular Plan - Monthly Dividend Option', 'Axis Overnight Fund - Regular Plan - Monthly Dividend Option'), ('Axis Overnight Fund - Regular Plan - Weekly Dividend Option', 'Axis Overnight Fund - Regular Plan - Weekly Dividend Option'), ('Axis Liquid Fund - Direct plan - Bonus Option', 'Axis Liquid Fund - Direct plan - Bonus Option'), ('Axis Liquid Fund - Direct Plan - Daily Dividend Option', 'Axis Liquid Fund - Direct Plan - Daily Dividend Option'), ('Axis Liquid Fund - Direct Plan - Growth Option', 'Axis Liquid Fund - Direct Plan - Growth Option'), ('Axis Liquid Fund - Direct Plan - Monthly Dividend Option', 'Axis Liquid Fund - Direct Plan - Monthly Dividend Option'), ('Axis Liquid Fund - Direct Plan - Weekly Dividend Option', 'Axis Liquid Fund - Direct Plan - Weekly Dividend Option'), ('Axis Liquid Fund - Regular Plan - Daily Dividend Option', 'Axis Liquid Fund - Regular Plan - Daily Dividend Option'), ('Axis Liquid Fund - Regular Plan - Growth Option', 'Axis Liquid Fund - Regular Plan - Growth Option'), ('Axis Liquid Fund - Regular Plan - Monthly Dividend Option', 'Axis Liquid Fund - Regular Plan - Monthly Dividend Option'), ('Axis Liquid Fund - Regular Plan - Weekly Dividend Option', 'Axis Liquid Fund - Regular Plan - Weekly Dividend Option'), ('Axis Liquid Fund - Retail Plan - Daily Dividend Option', 'Axis Liquid Fund - Retail Plan - Daily Dividend Option'), ('Axis Liquid Fund - Retail Plan - Growth Option', 'Axis Liquid Fund - Retail Plan - Growth Option'), ('Axis Liquid Fund - Retail Plan - Monthly Dividend Option', 'Axis Liquid Fund - Retail Plan - Monthly Dividend Option'), ('Axis Liquid Fund - Retail Plan - Weekly Dividend Option', 'Axis Liquid Fund - Retail Plan - Weekly Dividend Option'))
    date = datetime.today() - timedelta(days=1)
    MAX_DATE = date.strftime('%Y-%m-%d')
    mutual_fund_name = forms.ChoiceField(choices=MUTUAL_FUND, required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Mutual Fund Name', 'autocomplete': 'off'}))
    investment_amount = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Investment Amount', 'autocomplete': 'off', 'min': '1'}))
    investment_date = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(
        format=['%Y-%m-%d'], attrs={'class': 'form-control', 'type': 'date', 'min': "2015-01-01", 'max': MAX_DATE}))
    units = forms.FloatField(required=False)

    class Meta:
        model = investment
        fields = '__all__'

    def clean_units(self):
        investment_date = self.cleaned_data['investment_date']
        mf_data = get_data(str(investment_date))
        try:
            per_unit = float(mf_data[self.cleaned_data['mutual_fund_name']])
        except KeyError as e:
            raise ValidationError("Mutual Fund not found that date.")
        units = float(self.cleaned_data['investment_amount']) / per_unit
        return round(units, 2)

    def clean_investment_amount(self):
        investment_amount = int(self.cleaned_data['investment_amount'])
        if investment_amount < 0:
            raise ValidationError('Investment date cannot be less than.')
        return investment_amount
