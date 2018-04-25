#_*_coding:utf-8_*_
__author__ = 'jidong'

from django import forms
from iasset.models import Asset,Blade,BladeCenter,Network,Others,Parts
from iasset.models import Security,Server,Storage,Tape,VM,IDC,Cabinet
from inetwork.models import Ports

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_number','name','sn','model',
                  'purchase_date','warranty_period','expire_date','cost',
                  'renewal_date','renewal_cost','total_cost','asset_admin',
                  'status','online_date','offline_date','create_person','qrcode',
                  'picture','memo']
        # exclude = ['contract']

class BladeForm(forms.ModelForm):
    class Meta:
        model = Blade
        fields = '__all__'
        # exclude = ['asset']

class BladeCenterForm(forms.ModelForm):
    class Meta:
        model = BladeCenter
        fields = '__all__'
        # exclude = ['asset']

class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = '__all__'
        # exclude = ['asset']

class OthersForm(forms.ModelForm):
    class Meta:
        model = Others
        fields = '__all__'
        # exclude = ['asset']

class PartsForm(forms.ModelForm):
    class Meta:
        model = Parts
        fields = '__all__'
        # exclude = ['asset']

class SecurityForm(forms.ModelForm):
    class Meta:
        model = Security
        fields = '__all__'
        # exclude = ['asset']

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'
        # exclude = ['asset']

class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = '__all__'
        # exclude = ['asset']

class TapeForm(forms.ModelForm):
    class Meta:
        model = Tape
        fields = '__all__'
        # exclude = ['asset']

class VmForm(forms.ModelForm):
    class Meta:
        model = VM
        fields = '__all__'
        # exclude = ['asset']

class IdcForm(forms.ModelForm):
    class Meta:
        model = IDC
        # fileds = ['name','address','contact','status','isself','contract','cost','start_date','end_date','memo']
        # fields = '__all__'
        exclude = ['contract']




class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = '__all__'

    # def clean(self):
    #     try:
    #         name = self.cleaned_data["name"]
    #     except Exception as e:
    #         raise forms.ValidationError(e)
    #     is_name_exist = Cabinet.objects.filter(name=name).exists()
    #     if is_name_exist:
    #         raise forms.ValidationError(u"%s 已存在" % name)
    #     return self.cleaned_data


class PortsForm(forms.ModelForm):
    class Meta:
        model = Ports
        fields = '__all__'
