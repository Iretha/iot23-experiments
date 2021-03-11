# ml-experiments-iot23
ML experiments with IoT23 dataset [1]

## 1. Prerequisites (Tools & Technologies)
No  | Name          | Description
--- |------------   |-------------
1   | [Python 3.8](https://www.python.org/downloads/release/python-380/)|   Programming Language 
2   | [scikit-learn](https://scikit-learn.org/stable/)| Tools for Machine Learning in Python
3   | [NymPy](https://numpy.org/)| Tools for Scientific Computing in Python
4   | [pandas](https://pandas.pydata.org/)| Tools for Data Analysis & Data Manipulation in Python
5   | [pickle](https://docs.python.org/3/library/pickle.html)| Python object serialization for model serialization
6   | [pyplot]()|
7   | [seaborn]()|


## 2. How to run this example
1. Download & Extract [IoT23](https://www.stratosphereips.org/datasets-iot23)
2. Clone this repo
3. Open **config.py** and modify "iot23_dataset_location" to point to "iot23_small" folder from the dataset
4. Create new output folder for the output files
5. Open **config.py** and modify "iot23_output_directory" to point to the newly created output folder


---
[1] “Stratosphere Laboratory. A labeled dataset with malicious and benign IoT network traffic. January 22th. Agustin Parmisano, Sebastian Garcia, Maria Jose Erquiaga. 
Online: https://www.stratosphereips.org/datasets-iot23
