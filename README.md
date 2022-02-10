# Web-map project 
Web map is an application made with Python library "Folium" which is based on JS "LeafLet" library

To use this module, firstly you have to install all dependencies or enable virtual environtment

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

## Instalation
To install folium
```bash
pip install folium
```
To install geopy
```bash
pip install geopy
```
To install haversine
```bash
pip install haversine
```

## Or use this command to enable virtual environment
```bash
pipenv shell
```

## Usage
```bash
python main.py "year" "latitude" "longitude"
```

## Example of generated map
year: 2003; 
latitude: 12; 
longitude: 32; 
<img width="1440" alt="Знімок екрана 2022-02-10 о 13 43 20" src="https://user-images.githubusercontent.com/59284695/153402355-a1bb6a90-78b8-4026-8648-caf19afc81b6.png">

Map has 4 layers:
* Map
* Markers
* Area of filming (optional)
* distance (optional)

# Information about project
As we can see, this web-map shows us ten the nearest places where films of the given year were filmed. Every marker has a short description (you can see it after clicking on it) about each movie (name of the film and year). Also, there are some additional layers that you can toggle by the button above. These allow you to see the distance between the given place and the place of filming and the area of filming.
