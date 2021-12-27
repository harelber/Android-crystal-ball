### This directory contains the MB attacks. Each attack needs the following inputs:


## MB1
First, run the drebin classifier following:
https://github.com/MLDroid/drebin
Then, run the run_disect.py in the MB1 folder file with the following inputs:
1. A path to the output folder.
2. path to the explanations json file. If you run holdout classification, the path is for explanations_HC.json. Else, the path is for explanations_RC.json.
3. A path to the input folder.
4. A path the APK key for signing.
## MB2 and MB3
1. A path to the output folder.
2. apk key for signing the app.
3. A path to the input folder.

The MB2 attack uses the statistics.csv file, that depict the use of permission requests in the dataset. An example for such a file can be viewed in this folder.
