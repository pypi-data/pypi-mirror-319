# Python Library: `ChemDescriptors`

This library provides various functions for calculating molecular descriptors and fingerprints in cheminformatics. It supports the calculation of a wide range of molecular descriptors and fingerprints, such as RDKit, Lipinski, Morgan, Mordred, and more.

## Importance of Fingerprint Types:
- **Distinct Representation:** Different fingerprint types capture various aspects of a molecule’s structure, allowing for versatile molecular comparisons.
- **Diverse Applications:** Depending on the task (such as similarity searching, classification, or clustering), choosing the right fingerprint type ensures better performance in chemical analysis and predictive modeling.
- **Accuracy in Modeling:** The right fingerprint type can significantly improve the accuracy of machine learning models and predictions based on molecular features.


## Number of Fingerprints:
The library supports a wide variety of fingerprint types, enabling a range of analyses for molecular datasets.

## Tutorial & Example visit the Chemical Descriptors Repository. [GitHub Repository](https://gist.github.com/AhmedAlhilal14/0efb8ff1b15c1227367cacea6ae16e2c#file-chemdescriptors-tutorial-ipynb) & [GitHub Repository]( https://github.com/AhmedAlhilal14/chemical-descriptors)

## Functions

### **add_rdkit_descriptor**(input_file,smiles_column)

**Description:**  
This function calculates RDKit molecular descriptors for molecules specified in a CSV file (`input_file`) using SMILES strings from a specified column (`smiles_column`). The calculated descriptors are appended as additional columns to the original data and saved in a new CSV file named `<input_file_name>_rdkit_descriptor.csv`.

**Parameters:**
- `input_file` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.

**Output:**  
The output will be saved as a CSV file named `<input_file_name>_rdkit_descriptor.csv`.

---

### **add_lipinski_descriptors**(file_path, smiles_column, verbose=False)

**Description:**  
This function calculates Lipinski descriptors for molecules specified in a CSV file (`file_path`) using SMILES strings from a specified column (`smiles_column`). It automatically saves the calculated descriptors to an output file named `<input_file_name>_lipinski_descriptors.csv`.

**Parameters:**
- `file_path` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.
- `verbose` (bool, optional): If `True`, the function will print additional processing details. Default is `False`.

**Output:**  
The output will be saved as a CSV file named `<input_file_name>_lipinski_descriptors.csv`.

---

### **add_morgan_fp**(input_file, smiles_column)

**Description:**  
Calculates Morgan fingerprints for molecules specified in a CSV file (`input_file`) using SMILES strings from a specified column (`smiles_column`). The function saves the calculated fingerprints to an output file named `<input_file_name>_calculate_morgan_fpts.csv`.

**Parameters:**
- `input_file` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.

**Output:**  
The output will be saved as a CSV file named `<input_file_name>_calculate_morgan_fpts.csv`.

---

### **add_mordred_descriptors**(input_file, smiles_column)

**Description:**  
Computes Mordred descriptors for molecules specified in a CSV file (`input_file`) using SMILES strings from a specified column (`smiles_column`). The function saves the computed descriptors to an output file named `<input_file_name>_mordred_descriptors.csv`.

**Parameters:**
- `input_file` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.

**Output:**  
The output will be saved as a CSV file named `<input_file_name>_mordred_descriptors.csv`.

---


**add_WienerIndex_ZagrebIndex(filename, smiles_column):


### **add_WienerIndex_ZagrebIndex**(input_file, smiles_column)

**Description:**  
Computes WienerIndex and ZagrebIndex descriptors for molecules specified in a CSV file (`input_file`) using SMILES strings from a specified column (`smiles_column`). The function saves the computed descriptors to an output file named `add_WienerIndex_ZagrebIndex_<input_file_name>_.csv`.

**Parameters:**
- `input_file` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.

**Output:**  
The output will be saved as a CSV file named `<input_file_name>_mordred_descriptors.csv`.

---
### **add_padelpy_fps**(input_file, smiles_column)

**Description:**  
This function allow to user to add  12 different types of molecular fingerprints  by using padelpy Library.. The supported fingerprints include:

- `AtomPairs2DCount`
- `AtomPairs2D`
- `EState`
- `CDKextended`
- `CDK`
- `CDKgraphonly`
- `KlekotaRothCount`
- `KlekotaRoth`
- `MACCS`
- `PubChem`
- `SubstructureCount`
- `Substructure`

Each enhanced dataset with fingerprints is saved as separate CSV files, appended with the respective fingerprint type name.

**Parameters:**
- `input_file` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.
- `Then run the code`: You find list of fingerpints you can select one or more to add them in your file

**Output:**  
Each fingerprint type will be saved as a separate CSV file with the respective fingerprint type name appended.  
For example: `<input_file_name>_AtomPairs2DCount.csv`.

---

### **add_molfeat_fps**(filename, smiles_column)

**Description:**  
This function allow to user to add  19 different types of molecular fingerprints by using molfeat Library. The supported fingerprints include:

  - `maccs`
  - `avalon`
  - `pattern`
  - `layered`
  - `map4`
  - `secfp`
  - `erg`
  - `estate`
  - `avalon-count`
  - `ecfp`
  - `fcfp`
  - `topological`
  - `atompair`
  - `rdkit`
  - `ecfp-count`
  - `fcfp-count`
  - `topological-count`
  - `atompair-count`
  - `rdkit-count`

### Parameters:
- `filename` (str): Path to the input CSV file containing molecular data in SMILES format.
- `smiles_column` (str): The name of the column in the input CSV file that contains the SMILES strings.
- `Then run the code`: You find list of fingerpints you can select one or more to add them in your file


### Output:
The output will be saved as a CSV file named `<input_file_name>_<fp_type>.csv` depending on the fingerprint type chosen.




### Refernce:
1. Emmanuel Noutahi, Cas Wognum, Hadrien Mary, Honoré Hounwanou, Kyle M. Kovary, Desmond Gilmour, thibaultvarin-r, Jackson Burns, Julien St-Laurent, t, DomInvivo, Saurav Maheshkar, & rbyrne-momatx. (2023). datamol-io/molfeat: 0.9.4 (0.9.4). Zenodo. [https://doi.org/10.5281/zenodo.8373019](https://doi.org/10.5281/zenodo.8373019)  
   [GitHub Repository](https://github.com/datamol-io/molfeat/tree/main)

2. RDKit: Open-source cheminformatics software. [https://rdkit.org](https://rdkit.org)

3. Moriwaki, H., Tian, YS., Kawashita, N. et al. (2018). Mordred: a molecular descriptor calculator. *Journal of Cheminformatics*, 10, 4. [https://doi.org/10.1186/s13321-018-0258-y](https://doi.org/10.1186/s13321-018-0258-y)

4. PaDELPy: A Python wrapper for PaDEL-Descriptor software. [GitHub Repository](https://github.com/ecrl/padelpy)

5. Ahmed Alhilal. Chemical Descriptors Repository. [GitHub Repository](https://github.com/AhmedAlhilal14/chemical-descriptors)
