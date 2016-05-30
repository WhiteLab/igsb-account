from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
import ldap
import ldap.modlist as modlist

from igsb_account.local_settings import LDAP_URL, LDAP_BIND_CN, LDAP_PASSWORD


def home(request):
    request.session['app_name'] = request.POST.get('app_name', '')
    request.session['app_redirect_url'] = request.POST.get('app_redirect_url', '')
    return render(request, 'account/home.html')


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
            return HttpResponseRedirect(reverse_lazy('create_already_exists', args=(username,)))

        igsb_ldap.unbind_s()

        return HttpResponseRedirect(reverse_lazy('create_success', args=(username,)))

    return HttpResponseRedirect(reverse_lazy('create_error'))


def create_success(request, account_name):
    return render(request, 'account/success.html', {
        'account_name': account_name,
        'app_name': request.session.get('app_name', ''),
        'app_redirect_url': request.session.get('app_redirect_url', '')
    })


def create_already_exists(request, account_name):
    return render(request, 'account/already_exists.html', {'account_name': account_name})
