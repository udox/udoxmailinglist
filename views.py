import datetime
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.forms.extras import widgets
from django.http import Http404, HttpResponse, HttpResponseRedirect

from udoxmailinglist import models
from udoxcore.models import GENDER_CHOICES
from udoxrecaptcha import ReCaptchaField


class SignupForm(forms.ModelForm):
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, required=False)
    now = datetime.datetime.now()
    dob = forms.DateField(widget=widgets.SelectDateWidget(years=range(now.year,1900,-1)), required=False)
    interest_items = forms.ModelMultipleChoiceField(queryset=models.InterestItem.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    captcha = ReCaptchaField()

    class Meta:
        model = models.Member


def signup(request):
    status = 200
    if request.method == 'POST':
        form = SignupForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save()
            if request.is_ajax():
                template = 'mailinglist/thankyou_message.html'
            else:
                template = 'mailinglist/thankyou.html'
            return render_to_response(template,
                {},
                context_instance=RequestContext(request)
            )
        else:
            status = 400
    else:
        form = SignupForm()
    
    interests = models.InterestItem.objects.all()
    
    if request.is_ajax():
        template = 'mailinglist/signup_form.html'
    else:
        template = 'mailinglist/signup.html'
    
    return HttpResponse(
        render_to_string(template,
            {
                'form': form,
                'interests': interests,
            },
            context_instance=RequestContext(request)
        ),
        status=status,
    )

def mobile_signup(request):
    status = 200
    if request.method == 'POST':
        form = SignupForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.save()
            template = 'mailinglist/mobile_thankyou.html'
            return render_to_response(template,
                {},
                context_instance=RequestContext(request)
            )
        else:
            HttpResponseRedirect("/signup/mobile/")
    else:
        form = SignupForm()
    
    interests = models.InterestItem.objects.all()
    
    template = 'mailinglist/mobile_signup.html'
    
    return HttpResponse(
        render_to_string(template,
            {
                'form': form,
                'interests': interests,
            },
            context_instance=RequestContext(request)
        ),
        status=status,
    )
