import glob
import os
import zipfile
import copyrightRplacer
from io import BytesIO
from io import StringIO

def zipfiles(fileName, files):
  z = zipfile.ZipFile(fileName, 'w')
  for f in files:
    baseName = os.path.basename(f)
    dist = BytesIO()
    copedFile = copyrightRplacer.start(f, dist)
    z.writestr(f.split('&&')[1], copedFile.getvalue())
  z.close()

files = glob.glob('./download/**/*.pptx', recursive=True)
# files = files[0:3]
Map = {}

for fileName in files:
  baseName = os.path.basename(fileName)
  cate = baseName.split(',')[0]
  if cate in Map:
    Map[cate].append(fileName)
  else:
    Map[cate] = [fileName]

# cates = list(Map.keys())
# for cate in cates:
#   files = Map.get(cate)
#   zipfiles(f'./dist/{cate}.zip', files)

files2 = Map['工作汇报']
Map2 = {}
for fileName in files2:
  baseName = os.path.basename(fileName)
  cate = baseName.split(',')[1]
  if cate in Map2:
    Map2[cate].append(fileName)
  else:
    Map2[cate] = [fileName]

cates = list(Map2.keys())
for cate in cates:
  files = Map2.get(cate)
  if cate not in ['党政机关', '教学课件', '毕业答辩']:
    continue
  # print(f'{cate} : {len(files)}')
  zipfiles(f'./dist2/{cate}.zip', files)
