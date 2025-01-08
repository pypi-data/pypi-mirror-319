# import os
# import sys
# import logging
# import pkg_resources
# from tqdm import tqdm
# import torch
# import joblib
# from ultralytics import YOLO
# from .imgprocessing import *
# from .classify import *
# from .predict import *
# from .output import *

# logging.getLogger('ultralytics').setLevel(logging.WARNING)
# models_dir = pkg_resources.resource_filename(__name__, 'models')
# MPATH = os.path.join(models_dir, 'detection.pt')
# MODEL = YOLO(MPATH)
# QPATH = os.path.join(models_dir, 'qcmodel.pkl')
# home_dir = os.path.expanduser('~')
# ipath = os.path.join(home_dir, 'imagetiles')
# DPATH = ''
# OPATH = os.path.join(home_dir, 'output')
# IMGSZ = 640

# class countblood():
#     def __init__(self, path, devicenum=-1):
#         self.path = path
#         self.devicenum = devicenum
#         if self.devicenum == -1:
#             print('CPU selected.')
#             self.devicenum = 'cpu'
#         elif torch.cuda.is_available() and devicenum < torch.cuda.device_count():
#             print('Selected GPU available.')
#             print('GPU number : ', devicenum)
#         else:
#             i = input('The selected device is not available. Use CPU? ([y]/n) ')
#             if i == 'y' or i == '':
#                 print('CPU selected.')
#                 devicenum = 'cpu'
#             else:
#                 print('No available device selected.')
#                 print('Program exit.')
#                 exit()
#         # Load qc model
#         qcmodel = torch.load(QPATH, map_location=torch.device(devicenum))
#         qcmodel.eval()

#         # Create necessary folders
#         if os.path.exists(PATH):
#             try:iname = PATH.split('/')[-1]
#             except:iname = PATH.split('\\')[-1]
#             iname = iname[:-5]
#             IPATH = os.path.join(ipath, iname)
#             DPATH = os.path.join(IPATH, 'discard')
#             try:os.makedirs(IPATH)
#             except:pass
#             try:os.makedirs(DPATH)
#             except:pass
#             try:os.makedirs(OPATH)
#             except:pass
#         else:
#             print('NDPI file does not exist. Please check the path.')
#             return 0

#         # If ndpi file exists
#         qclist = [0, 0, 0]
#         counts = []
#         total_count = [0 for _ in range(10)]
#         width, height = dimensions(PATH)

#         # tqdm progress bar for image cut and prediction
#         total_progress = len(range(0, width, IMGSZ)) * len(range(0, height, IMGSZ))
#         progress_bar = tqdm(total=total_progress, desc='Cutting image')

#         # Cut ndpi into 640px size small images
#         for i in range(0, width, IMGSZ):
#             for j in range(0, height, IMGSZ):
#                 outimg = cutimg(PATH, i, j, IMGSZ)
#                 isStandard = classify(qcmodel, outimg, devicenum)
#                 qclist[isStandard] += 1

#                 progress_bar.update(1)

#                 # Save image if standard, discard if not standard
#                 if isStandard != 2:
#                     # saveimg(DPATH, outimg, i, j)
#                     continue
#                 counts.append(predict(MODEL, outimg, devicenum))
    
#         # tqdm progress bar for counting
#         total_progress = len(counts)
#         progress_bar = tqdm(total=total_progress, desc='Counting cells')
#         for count in counts:
#             for c in zip(count[0], count[1]):
#                 if int(c[0]) == 10: continue
#                 total_count[int(c[0])] += int(c[1])
#             progress_bar.update(1)
        
#         output(OPATH, iname, total_count, qclist)