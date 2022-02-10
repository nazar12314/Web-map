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
<img width="1440" alt="Знімок екрана 2022-02-09 о 10 28 51" src="https://user-images.githubusercontent.com/59284695/153401664-c85ed36c-c1d6-4f96-82c2-d5ec9037d72f.png">

Map has 4 layers:
* Map
* Markers
* Area of filming
* distance
