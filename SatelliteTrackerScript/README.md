# Satellite-Tracker-Script
Satellite-Tracker-Script is a program to obtain satellite information via the [N2YO API](https://www.n2yo.com/).

## Features
- The search for satellites is conducted based on the coordinates provided as parameters; 
- This process is repeated according to the user's specifications;
- The repetition of searches is determined by the time period set by the user;
- Upon completion of the searches, a log is generated and stored in the logs folder, containing details of all searches conducted;
- Additionally, a xlsx file is generated containing data on the appearance of each satellite. In this file, an "X" is marked in the cell corresponding to the time at which a particular satellite was sighted.


## Run Locally

Clone the project
```bash
  git clone https://github.com/Pedrohsgarci4/Satellite-Tracker-Script.git
```

Go to the project directory
```bash
  cd Satellite-Tracker-Script
```

Install dependencies
```bash
  pip install geopy requests openpyxl
```

Run the program with the following arguments:
- `lat: float`: satellite footprint latitude (decimal degrees format);
- `lng: float`: satellite footprint longitude (decimal degrees format);
- `alt: float`: satellite altitude (km);
- `category_id`: category id (see the [API reference](https://www.n2yo.com/api/) for more details);
- `steps: int`: number of steps to execute the program;
- `delay: float`: delay between steps (in seconds).

Example of program execution:
```bash
python3 main.py -24.7875286 -55.768967 90 52 5760 15
```
## Support

If you have any questions or suggestions, please contact us by email: gabrielprates.aluno@unipampa.edu.br or pedrosachete.aluno@unipampa.edu.br.

