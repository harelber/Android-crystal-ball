import os
import sys
import time
import glob
import shutil
import pickle

def end_file_process(f,folder,APK_KEY):#sign and copy apk
	f=f.split('/')[-1].split(".apk")[0]
	os.system("apktool b "+f)#+" 2>&1")
	file_to_sign=f+"/dist/"+f+".apk"
	os.system("jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass apkkey -keystore apkkey.keystore "+file_to_sign+" alias_name >> tmp.csv")
	os.remove("tmp.csv")
	os.system("cp "+file_to_sign+" "+folder+"/")#copy to new apks
	shutil.rmtree(f)#remove app open pack

def open_apk(f):#read the manifest
	os.system("apktool -f d "+f)#open apk
	folder_name=f.split('/')[-1].split(".apk")[0]
	with open(folder_name+"/AndroidManifest.xml","r") as r:
		content=r.readlines()
	r.close()
	return content,folder_name

def write_attack(content,folder_name,f,output,APK_KEY):#create clear manifest
	os.remove(folder_name+"/AndroidManifest.xml")

	with open(folder_name+"/AndroidManifest.xml", "w") as w:
		for c in content:
			w.write(c)
	end_file_process(f,output,APK_KEY)

def get_applications(PATH_TO_FILES):
	files=[]
	for i in range(0,5):
		P=PATH_TO_FILES.replace("_i","_"+str(i))
		for path, subdirs, files_w in os.walk(P):
			for name in files_w:
				n=os.path.join(path, name)
				if not n.endswith(".apk"):
					continue
				files.append(name)
	return files

def get_applications_allready(PATH_TO_FILES):
	files=[]
	for path, subdirs, files_w in os.walk(PATH_TO_FILES):
		for name in files_w:
			n=os.path.join(path, name)
			if not n.endswith(".apk"):
				continue
			files.append(name)
	return files

	
PATH_TO_FILES_DONE=sys.argv[1]
APK_KEY=sys.argv[3]
files=os.listdir(sys.argv[2])


#iterate files
for f in files:
    #locate the folder
    check=sys.argv[2]+"/"+f
    if os.path.isfile(check):
        f=check

        try:
	        #first attack
	        content,folder_name=open_apk(f)#read the apk
	        for c in range(0,len(content)):
		        if "uses-permission " in content[c]:
			        content[c]=content[c].replace("uses-permission ","uses-permission-sdk-23 ")
	        write_attack(content,folder_name,f,PATH_TO_FILES_DONE,apk_key)
        except Exception as e:
                try:
                        shutil.rmtree(f)#remove app open pack
                except:
                        continue