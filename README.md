## Source files:

`generate.py`: Build the static HTML file

`priority_points.csv`: Assign "points" to each resource, ordering within file indicates priority. (Fibonacci sequence: 1,2,3,5,8,13,21)

`module_list.csv`: The list of resource Modules

`boot.html.j2`: The HTML Template

`settings.py`: Values used to build timeline

## Settings

See the settings.py file.

## Usage

`pip install jinja2`

`python generate.py`

(developed and test using python3.7.2)
