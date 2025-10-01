from django import forms 
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta :
        model = Transaction
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput #user er theke hide kora thakbe

    
    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance # 500tk , 5000tk deposit korvo tokon total balance  hobe 5500
        return super().save()
    

class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam , 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'you need to deposit at least {min_deposit_amount}$'
            )
        return amount
    

class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance 
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'you can withdraw at least {min_withdraw_amount}$'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'you can withdraw at most {max_withdraw_amount} $'
            )
        
        if amount > balance: # amount=5000, tar balance ache 200
            raise forms.ValidationError(
                f'you have {balance} $ in your account.'
                'you can not withdraw more than you account balance'
            )
        
        return amount
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        return amount