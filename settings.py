from datetime import datetime

# The sarting date of all work
START_DATE = datetime(2019, 4, 1)

# The number of FTEs assigned to devleopment
FTES = 5

# The percent of time each FTE will spend
PERCENT_ALLOCATED = .7

# The number of weeks per sprint
SPRINT_WKS = 2

# The number of hours est per point
HRS_PER_POINT = 8


HOURS_PER_SPRINT = SPRINT_WKS * 40 * PERCENT_ALLOCATED * FTES
TL_GROUPS = ["Ansible Releases",
             "Network Collection Releases",
             "Sprints",
             "Foundation",
             "Operations",
             "Policy",
             "Services",
             "Topology"]

ANSIBLE_RELEASES = [
    {"name": "2.8", "note": "", "date": datetime(2019, 5, 1)},
    {"name": "2.9", "note": "(est)", "date": datetime(2019, 10, 1)},
    {"name": "2.10", "note": "(est)", "date": datetime(2020, 5, 1)},
    {"name": "2.11", "note": "(est)", "date": datetime(2020, 10, 1)},
    {"name": "2.12", "note": "(est)", "date": datetime(2021, 5, 1)},
    {"name": "2.13", "note": "(est)", "date": datetime(2021, 10, 1)},
    {"name": "2.14", "note": "(est)", "date": datetime(2022, 5, 1)}
    ]

NETWORK_COLLECTION_RELEASE_CADENCE_WKS = 2
