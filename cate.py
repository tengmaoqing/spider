import glob
import os
import zipfile

def zipfiles(fileName, files):
  z = zipfile.ZipFile(fileName, 'w')
  for f in files:
    baseName = os.path.basename(f)
    z.write(f, f.split('&&')[1])
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

cates = list(Map.keys())
for cate in cates:
  files = Map.get(cate)
  zipfiles(f'./dist/{cate}.zip', files)


