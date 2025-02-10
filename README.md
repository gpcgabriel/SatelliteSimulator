# SatelliteSimulator

**SatelliteSimulator** is a simulator for service offloading on Low-Earth Orbit (LEO) satellites. It implements the OLEO heuristic and other reference approaches. For more details, check our article available in the DOI. As future work, we aim to parameterize satellites and develop new heuristics to improve Quality of Service (QoS).

## 📦 Installation
To install and set up the project, run the following commands:

1. Initialize the Git repository:
```bash
git init
```

2. Add the remote repository:
```bash
git remote add origin https://github.com/gpcgabriel/SatelliteSimulator.git
```

3. Fetch the latest version of the code:
```bash
git pull origin main
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage
To run the simulation, modify `dataset/simulation.json` config file and use the following command:
```bash
python3 main.py
```

Or configure optional parameters:
```bash
python3 main.py -v <verbosity_level> -o <output_file_path> -c <config_file_path>
```

- **Verbosity level (`-v`)**:
  - `0`: Displays only the status when a new algorithm starts.
  - `1`: Displays the state of each service at every step.
- **Output file (`-o`)**: Defines the path where the final JSON with metrics will be saved. 
- **Configuration file (`-c`)**: Contains detailed specifications of the simulation.

## 🚨 Notes:
- To modify the number of simulation steps, edit the `general_utilities.py` file.
- Graphics are available at `graphics/` directory.


## 👥 Authors
- [@gpcgabriel](https://www.github.com/gpcgabriel)
- [@diogo2m](https://www.github.com/diogo2m)
- [@mcluizelli](https://www.github.com/mcluizelli)

## 📩 Support

For questions or suggestions, contact us at:
✉️ gabrieprates.aluno@unipampa.edu.br  
✉️ diogomonteiro.aluno@unipampa.edu.br

