from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='/login/')
def admin_page(request):
    return render(request, 'admin/admin_page.html')