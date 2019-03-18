from datetime import timedelta, datetime
from jinja2 import Template
import csv
import settings

def build_ansible_releases():
    ars = []
    settings.ANSIBLE_RELEASES.sort(key=lambda x: x['date'])
    for release in settings.ANSIBLE_RELEASES:
        ars.append({"start": release['date'].isoformat(),
                    "start_human": release['date'].strftime('%Y-%m-%d'),
                    "className": "ansibleRelease",
                    "content": "%s %s" % (release['name'], release['note']),
                    "group": settings.TL_GROUPS.index("Ansible Releases")})
    return ars

def build_resource_modules():
    modules = []
    module_list = [dict(m) for m in csv.DictReader(open("module_list.csv"))]
    priority_points = [dict(m) for m in csv.DictReader(open("priority_points.csv"))]
    for idx, ppts in enumerate(priority_points):
        ppts['priority'] = idx
    for module in module_list:
        ppts = next(p for p in priority_points if p['resource'] == module['resource'])
        module['priority'] = ppts['priority']
        module['points'] = ppts['points']
    module_list.sort(key=lambda x: x['priority'])
    for module in module_list:
        task_duration = int(module['points']) * settings.HRS_PER_POINT
        groups_lowered = [g.lower() for g in settings.TL_GROUPS]
        tipe = module['type'].split('/')[0]
        modules.append({"className": tipe,
                        "content": module['name'],
                        "group": groups_lowered.index(tipe),
                        "kind": "resource_module",
                        "duration": task_duration})
    return modules

def build_sprints(resource_modules):
    sprs = []
    sprint_end = settings.START_DATE + timedelta(weeks=settings.SPRINT_WKS)
    sprint_num = 1
    rm_with_dates = []
    while resource_modules:
        sprint = {'className': 'sprint',
                  'group': 2,
                  'content': str(sprint_num),
                  'start': sprint_end.isoformat(),
                  'start_human': sprint_end.strftime('%Y-%m-%d'),
                  'resource_modules': [],
                  'total': 0}
        for resource_module in resource_modules[:]:
            if sprint['total'] + resource_module['duration'] > settings.HOURS_PER_SPRINT:
                continue
            else:
                sprint['resource_modules'].append(resource_module)
                sprint['total'] += resource_module['duration']
                resource_module['start'] = sprint_end.isoformat()
                resource_module['start_human'] = sprint_end.strftime('%Y-%m-%d')
                rm_with_dates.append(resource_module)
                resource_modules.remove(resource_module)
        sprint_num += 1
        sprint_end += timedelta(weeks=settings.SPRINT_WKS)
        sprs.append(sprint)
    return sprs, rm_with_dates


def build_network_collection_releases(sprints):
    sprints = sprints.copy()
    ncrs = []
    delivered = []
    for idx, ansible_release in enumerate(settings.ANSIBLE_RELEASES):
        anc_release_version = 1
        for sprint in sprints[:]:
            sprint_start = datetime.fromisoformat(sprint['start'])
            if sprint_start < ansible_release['date']:
                delivered.extend(sprint['resource_modules'])
                sprints.remove(sprint)
                continue
            if ansible_release['date'] <= sprint_start < settings.ANSIBLE_RELEASES[idx+1]['date']:
                delivered.extend(sprint['resource_modules'])
                sprints.remove(sprint)
                ncrs.append({"start": sprint['start'],
                             "start_human": sprint_start.strftime('%Y-%m-%d'),
                             "className": "ansibleNetworkCollectionRelease",
                             "content": "%s.%s" % (ansible_release['name'], anc_release_version),
                             "group": settings.TL_GROUPS.index("Network Collection Releases"),
                             "resource_modules": delivered})
                anc_release_version += 1
                delivered = []
    return ncrs

def template(dates):
    dates.sort(key=lambda x: datetime.fromisoformat(x['start']))
    # pprint(dates)
    with open('index.html.j2') as file_:
        tmplt = Template(file_.read())

    with open('index.html', encoding='utf-8', mode='w') as file:
        file.write(tmplt.render(dates=dates,
                                groups=settings.TL_GROUPS,
                                settings=settings))

def main():
    ansible_releases = build_ansible_releases()
    resource_modules = build_resource_modules()
    sprints, resource_modules = build_sprints(resource_modules)
    ncrs = build_network_collection_releases(sprints=sprints)
    template(ansible_releases + ncrs + resource_modules + sprints)

if __name__ == "__main__":
    main()
