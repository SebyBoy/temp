from django.shortcuts import render
from .models import Team, Department

def reports_page(request):
    department_id = request.GET.get('department')

    teams = Team.objects.all()

    if department_id:
        teams = teams.filter(department_id=department_id)

    departments = Department.objects.all()

    total_teams = teams.count()
    no_manager = teams.filter(manager__isnull=True)

    return render(request, 'reports.html', {
        'teams': teams,
        'departments': departments,
        'total_teams': total_teams,
        'no_manager': no_manager
    })


import csv
from django.http import HttpResponse
from .models import Team

def export_teams_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teams_report.csv"'

    writer = csv.writer(response)

    teams = Team.objects.all()
    total_teams = teams.count()
    no_manager = teams.filter(manager__isnull=True)

    # ===== SUMMARY =====
    writer.writerow(['REPORT SUMMARY'])
    writer.writerow(['Total Teams', total_teams])
    writer.writerow(['Teams Without Managers', no_manager.count()])
    writer.writerow([])

    # ===== TEAMS WITHOUT MANAGER =====
    writer.writerow(['Teams Without Managers'])
    for team in no_manager:
        writer.writerow([team.team_name])
    writer.writerow([])

    # ===== FULL TEAM TABLE =====
    writer.writerow(['All Teams'])
    writer.writerow(['Team Name', 'Department', 'Manager'])

    for team in teams:
        writer.writerow([
            team.team_name,
            team.department.department_name,
            team.manager.name if team.manager else 'No Manager'
        ])

    return response