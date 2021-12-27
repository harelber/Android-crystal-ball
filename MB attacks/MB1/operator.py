from __future__ import division
import os
import sys
import time
from shutil import move
from shutil import copyfile

Malware_train=sys.argv[4]
Benign_train=sys.argv[5]
Malware_test=sys.argv[1]+sys.argv[3]
Benign_test=sys.argv[6]

#Malware_test="/home/cyber/robust_apk_detection/attack/malware"


start=time.time()
os.chdir(sys.argv[7])
#First, run Drebin on the dataset
os.system("python Main.py --holdout 1 --testmaldir "+Malware_test+" --testgooddir "+Benign_test+" --maldir "+Malware_train+" --gooddir "+Benign_train)
copyfile("explanations_HC.json", "../explanations_former.json")#copy the weights
os.chdir("../")
#Then, get the dataset report from it,for each app
with open("Drebin/class_report.csv","r") as r:
        report=r.readlines()
r.close()
os.rename('Drebin/class_report.csv', 'Drebin/class_report_former.csv')
#read data from the report
mal_files_in_data=0
mal_files_to_manip=0
files_for_attack=[]
#create the dir of malware
directory="malware"
if not os.path.exists(directory):
    os.makedirs(directory)
#take the files that were identified
for line in report:
        line=line.split(",")
        name=line[0]
        truth=float(line[1])
        label=float(line[2])
        if truth==1:
                mal_files_in_data+=1
                if truth==label:#Drebin failed
                        files_for_attack.append(name.split(".")[0])
                        mal_files_to_manip+=1

prec_mal=mal_files_to_manip/mal_files_in_data       
#Then, run the attack on the apps that were identified correctly

for f in files_for_attack:
        try:
                os.system("cp "+f+".apk"+" malware/")
        except:
                continue

os.system("python read_disect.py malware/ "+sys.argv[2])
#check the files again

os.chdir("Drebin")

os.system("python Main.py --holdout 1 --testmaldir ../"+sys.argv[2]+" --testgooddir "+Benign_test+" --maldir "+Malware_train+" --gooddir "+Benign_train)
os.chdir("../")
#move important files
new_folder="subtle_manip"
os.mkdir(new_folder)
move(sys.argv[2],new_folder+"/")
move("Drebin/class_report.csv",new_folder+"/")
copyfile("Drebin/explanations_HC.json",new_folder+"/")
#Then, take part of the evaded apps and integrate them in the test data and test against other that were
#evasion' processed
mal_files_in_data=0
mal_files_to_manip=0
files_for_attack=[]
with open(new_folder+"/class_report.csv","r") as r:
        report=r.readlines()
r.close()
for line in report:
        line=line.split(",")
        name=line[0]
        truth=float(line[1])
        label=float(line[2])
        if truth==1:
                mal_files_in_data+=1
                if truth==label:#Drebin failed
                        files_for_attack.append(name.split(".")[0])
                        mal_files_to_manip+=1

prec_mal2=mal_files_to_manip/mal_files_in_data
#print prec_mal,prec_mal2#, prec_mal2   
end=time.time()
print "overall running time: "+str(end-start)+ " seconds"
