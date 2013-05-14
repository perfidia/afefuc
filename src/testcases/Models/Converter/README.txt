Skrypt konwertujący z formatu .mm (domyślny format dla programu FreeMind) do .XML

Sposób użycia:

./FreeMindToXMLConverter [input file] [output file] 

Struktura tworzonego pliku XML:

- główny element -> [start]
	- elementy podrzędne:
		- actor
		- text
		- action -> posiada atrybuty:
			- action -> w połączeniu z elementem object definiuje akcję do wykonania
		- value -> określa wartość
		- name -> określa nazwę elementu
		- url -> określa adres url
		- object -> określa rodzaj obiektu, na którym wykonana zostanie akcja - posiada atrybuty:
			- type -> określa typ obiektu
		- number -> określa wartość liczbową

