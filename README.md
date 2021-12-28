# Android-crystal-ball
This repository follows the Crystal Ball paper.

The results of the attacks against the VT scanners are presented in the VT_results folder.

The version of the Drebin model was taked from:
https://github.com/MLDroid/drebin

The implementation of Sec-SVM was kindly given to us by S2Lab:
https://s2lab.cs.ucl.ac.uk/projects/intriguing/

The DNN (basic DNN model from the repository) was taken from:
https://github.com/deqangss/adv-dnn-ens-malware

The re-implemenation of the FM model (based on https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8931539) used the implementation of Drebin. The changes are described in FM.txt.

The malicious apks can be obtained from the Drebin formal website:
https://www.sec.cs.tu-bs.de/~danarp/drebin/

An extended version of the benign dataset can be found in:
https://drive.google.com/file/d/1cDU-_K4q3fphwMlef7nJjZuIH7lPt3mN/view?usp=sharing

The code of the evasion attacks can be viewed in the MB attacks folder.

## Citation

```
@article{berger2021crystal,
  title={Crystal Ball: From Innovative Attacks to Attack Effectiveness Classifier},
  author={Berger, Harel and Hajaj, Chen and Mariconti, Enrico and Dvir, Amit},
  journal={IEEE Access},
  year={2021},
  publisher={IEEE}
}
