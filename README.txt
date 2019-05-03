# Intensity of mass spectrum prediction
Deep learning project for predicting fragment ion's intensity of theoretical spectrum

project directory
|-- resources # peptide sequence data and processing
    |-- jar_script_cptac.py
    |-- jar_script_pride.py
|-- scripts # data preprocessing script
    |-- peptide.py # peptide feature engineering
    |-- make_features_vector.py # feature vector to file
|-- src
    |-- main.py # learning and inference using DNN

This project is a graduation project for the semester of 2017-1. (Professor Eunok Paek)
The protein sequence was converted into a feature vector by feature engineering and then model learned and inferred using deep learning.
Although the result was not good, it was first tried in the BIS LAB. and it was selected as the excellent graduated project.
