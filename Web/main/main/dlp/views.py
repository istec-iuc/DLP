from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LogUpdateForm, PolicyCreateForm, PolicyUpdateForm, RuleCreateForm, RuleUpdateForm
from .models import Logs, Policy, Rule

import csv
import xlwt

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@login_required
def dashboard_views(request):

    return render(request, "dlp/dashboard.html")


@login_required
def policy_views(request):
    policy = Policy.objects.all()
    context = {
        'policy': policy
    }
    return render(request, "dlp/policy.html", context)


@login_required
def rules_views(request):
    rules = Rule.objects.all()
    context = {
        'rules': rules
    }
    return render(request, "dlp/rules.html", context)


@login_required
def logs_views(request):
    log_list = Logs.objects.all()

    paginator = Paginator(log_list, 15)  # Show 15 contacts per page

    page = request.GET.get('q')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        logs = log_list.filter(
            Q(file_path__icontains=query) | Q(event_type__icontains=query)).distinct()
    context = {
        'logs': logs
    }
    return render(request, "dlp/logs.html", context)

# only superuser


@login_required
def add_policy_views(request):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    if request.method == 'POST':
        policy_form = PolicyCreateForm(request.POST)
        if policy_form.is_valid():
            policy_form.save()
            messages.success(request, 'Policy has been created!')
            return redirect('dlp:policy')
        else:
            return render(request, 'dlp/post/add_policy.html', {'form': policy_form})

    policy_form = PolicyCreateForm(request.POST)
    return render(request, "dlp/post/add_policy.html", {'form': policy_form})


@login_required
def update_policy_views(request, id):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")
    instance = Policy.objects.get(pk=id)
    policy_form = PolicyUpdateForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if policy_form.is_valid():
            policy_form.save()
            messages.success(request, 'Policy has been updated!', {
                             'form': policy_form})
            return redirect('dlp:policy')
        else:
            return render(request, 'dlp/post/update_policy.html', {'form': policy_form})

    return render(request, "dlp/post/update_policy.html", {'form': policy_form})


@login_required
def delete_policy_views(request, id):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    policy = Policy.objects.get(id=id)
    try:
        policy.delete()
        messages.success(request, "Policy has been successfully deleted.")
    except:
        messages.error(request, "Policy could not be deleted!")

    return redirect('dlp:policy')


@login_required
def add_rule_views(request):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")
    rule_form = RuleCreateForm(request.POST or None)

    if request.method == 'POST':
        if rule_form.is_valid():
            rule_form.save()
            messages.success(request, 'Rule has been created!')
            return redirect('dlp:rules')
        else:
            return render(request, 'dlp/post/add_rule.html', {'form': rule_form})

    return render(request, 'dlp/post/add_rule.html', {'form': rule_form})


@login_required
def update_rule_views(request, id):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    instance = Rule.objects.get(id=id)
    rule_form = RuleUpdateForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if rule_form.is_valid():
            rule_form.save()
            messages.success(request, 'Rule has been updated!')
            return redirect('dlp:rules')
        else:
            return render(request, 'dlp/post/update_rule.html', {'form': rule_form})

    return render(request, 'dlp/post/update_rule.html', {'form': rule_form})


@login_required
def delete_rule_views(request, id):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    rule = Rule.objects.get(id=id)
    try:
        rule.delete()
        messages.success(request, "Rule has been successfully deleted.")
    except:
        messages.error(request, "Rule could not be deleted!")

    return redirect('dlp:rules')


@login_required
def update_log_views(request, id):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    instance = Logs.objects.get(id=id)
    log_form = LogUpdateForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if log_form.is_valid():
            log_form.save()
            messages.success(request, 'Log has been updated!')
            return redirect('dlp:logs')
        else:
            return render(request, 'dlp/post/update_log.html', {'form': log_form})

    return render(request, 'dlp/post/update_log.html', {'form': log_form})


@login_required
def delete_log_views(request, id):
    if not request.user.is_superuser:
        return redirect("dlp:dashboard")

    log = Logs.objects.get(id=id)
    try:
        log.delete()
        messages.success(request, "Log has been successfully deleted.")
    except:
        messages.error(request, "Log could not be deleted!")

    return redirect('dlp:logs')

# export


def logs_export_csv_views(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Logs_' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Source', 'Rule Type', 'Details'])

    logs = Logs.objects.all()

    for log in logs:
        writer.writerow([log.created_date, log.file_path,
                        log.rule_type, log.event_type])

    return response


def logs_export_excel_views(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Logs_' + \
        str(datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf*8')
    ws = wb.add_sheet('Logs')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Date', 'Source', 'Rule Type', 'Details']

    logs = Logs.objects.all()
    #  ws.write([log.created_date, log.file_path, log.rule_type, log.event_type])
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Logs.objects.all().values_list(
        'created_date', 'file_path', 'rule_type', 'event_type')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(rows[col_num]), font_style)

    wb.save(response)

    return response
