from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
import ldap
import ldap.modlist as modlist

from igsb_account.local_settings import LDAP_URL, LDAP_BIND_CN, LDAP_PASSWORD, ADMIN_EMAIL


def create_home(request):
    if 'app_name' not in request.session:
        request.session['app_name'] = request.POST.get('app_name', '')
        request.session['app_redirect_url'] = request.POST.get('app_redirect_url', '')
    return render(request, 'account/new/home.html')


def create(request):
    if request.POST:
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))

        igsb_ldap = ldap.initialize(LDAP_URL)
        igsb_ldap.simple_bind_s(LDAP_BIND_CN, LDAP_PASSWORD)

        dn = 'ou={},dc=igsb,dc=uchicago,dc=edu'.format(username)
        attrs = {
            'objectClass': 'organizationalUnit',
            'ou': username,
            'userPassword': password
        }

        ldif = modlist.addModlist(attrs)

        try:
            igsb_ldap.add_s(dn, ldif)
        except ldap.ALREADY_EXISTS:
            # Username already exists
            messages.add_message(request, messages.INFO, 'Account {} already exists.'.format(username))
            return HttpResponseRedirect(reverse_lazy('create_home'))

        igsb_ldap.unbind_s()

        return HttpResponseRedirect(reverse_lazy('create_success', args=(username,)))

    return HttpResponseRedirect(reverse_lazy('account_error'))


def create_success(request, account_name):
    return render(request, 'account/new/success.html', {
        'account_name': account_name,
        'app_name': request.session.get('app_name', ''),
        'app_redirect_url': request.session.get('app_redirect_url', '')
    })


"""
Change password views
"""


def change_password_home(request):
    if 'app_name' not in request.session:
        request.session['app_name'] = request.POST.get('app_name', '')
        request.session['app_redirect_url'] = request.POST.get('app_redirect_url', '')
    return render(request, 'account/change/home.html')


def change_password(request):
    if request.POST:
        username = str(request.POST.get('username'))
        old_password = str(request.POST.get('old-password'))
        new_password = str(request.POST.get('new-password'))

        igsb_ldap = ldap.initialize(LDAP_URL)
        igsb_ldap.simple_bind_s(LDAP_BIND_CN, LDAP_PASSWORD)

        dn = 'ou={},dc=igsb,dc=uchicago,dc=edu'.format(username)

        try:
            igsb_ldap.passwd_s(dn, old_password, new_password)
        except ldap.UNWILLING_TO_PERFORM:
            # Old password is not correct
            messages.add_message(request, messages.INFO, 'Password for account {} is incorrect.'.format(username))
            return HttpResponseRedirect(reverse_lazy('change_home'))

        igsb_ldap.unbind_s()

        return HttpResponseRedirect(reverse_lazy('change_success', args=(username,)))

    return HttpResponseRedirect(reverse_lazy('account_error'))


def change_success(request, account_name):
    return render(request, 'account/change/success.html', {
        'account_name': account_name,
        'app_name': request.session.get('app_name', ''),
        'app_redirect_url': request.session.get('app_redirect_url', '')
    })


def error(request):
    return render(request, 'account/error.html', {
        'admin_email': ADMIN_EMAIL
    })
