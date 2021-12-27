  
import os
import os.path
import sys
import time
import glob
import shutil
import random
import pickle

def end_file_process(f,folder,apkkey):#sign and copy apk

	f=f.split('/')[-1].split(".apk")[0]
        print f
        
	os.system("apktool b "+f)#+" 2>&1")
	file_to_sign=f+"/dist/"+f+".apk"
	os.system("jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass apkkey -keystore "+apkkey+" "+file_to_sign+" alias_name >> tmp.csv")
	os.remove("tmp.csv")
	os.system("cp "+file_to_sign+" "+folder)#copy to new apks
	shutil.rmtree(f)#remove app open pack


def open_apk(f):#read the manifest
	os.system("apktool -f d "+f)#open apk
	folder_name=f.split('/')[-1].split(".apk")[0]
	with open(folder_name+"/AndroidManifest.xml","r") as r:
		content=r.readlines()
	r.close()
	return content,folder_name

def write_attack(content,folder_name,f,output,apkkey):#create clear manifest
	os.remove(folder_name+"/AndroidManifest.xml")
        
	with open(folder_name+"/AndroidManifest.xml", "w") as w:
		for c in content:
			w.write(c)
	end_file_process(f,output,apkkey)


def get_applications(PATH_TO_FILES):
	files=[]
	for path, subdirs, files_w in os.walk(PATH_TO_FILES):
		for name in files_w:
			n=os.path.join(path, name)
			if not n.endswith(".apk"):
				continue
			files.append(name)
	return files

PATH_TO_FILES_DONE=sys.argv[1]

#read stats
with open("statistics.csv","r") as r:
	cont=r.readlines()
r.close()
by_mal=[]
by_ben=[]
for i in cont[1:]:
	line=i.split("{")
	line=line[2].split("}")
	family=line[0]
	stats=line[1].split(",")[1:3]
	benign=float(stats[0])
	by_ben.append([benign,family])
by_ben.sort(reverse=True)
perms_updated=[]
#need to be upgraded if families are in order
for p in by_ben[0:3]:
	ar_perms=[]
	temp_perms=p[1].split(",")
	for t in temp_perms:
		t=t.strip(" ").strip('"').strip("'")
		ar_perms.append('android.permission.'+t)
	perms_updated.append(ar_perms)


PATH_TO_FILES_DONE=sys.argv[1]
apk_key=sys.argv[3]
files=os.listdir(sys.argv[2])

#iterate files
family=""
for f in files:
        try:
	        family=perms_updated[random.randint(0,2)]
	        #second attack
	        content,folder_name=open_apk(f)#read the apk
	        #get a list of all permissions
	        current_app_perms={}
	        for c in range(0,len(content)):
		        if "uses-permission " in content[c]:
				        perm_temp=content[c].split('android:name=')[1].split('/')[0][1:-1]
				        current_app_perms[perm_temp]=0
	        
	        #create a dict of permissions of the app
	        for p in family:
		        current_app_perms[p]=1
	        #change the permissions to sdk-23 if needed
	        for c in range(0,len(content)):
		        if "uses-permission " in content[c]:
				        perm_temp=content[c].split('android:name=')[1].split('/')[0][1:-1]
				        if current_app_perms[perm_temp]==0:#not a member of the family with more than one member
					        content[c]=content[c].replace("uses-permission ","uses-permission-sdk-23 ")
	        #check if the family exists in the app-if not-create it
	        if not sum(current_app_perms.values())==len(family):# add another member to the family if not all the family is here
		        keys=[k for k,v in current_app_perms.items() if v == 1]
		        for k in keys:
			        for c in range(0,len(content)):
				        if "uses-permission " in content[c]:
					        content.insert(c,'<uses-permission android:name="'+k+'"/>')
					        break
	        write_attack(content,folder_name,f,PATH_TO_FILES_DONE,apk_key)
        except Exception as e:
                print f
                print e
	        continue
