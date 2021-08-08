import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys

for file in sys.argv[1:]:
    if not file[-4:] == '.i3d':
        raise Exception(f'File {file} is not an i3d file')
    else:
        filename = file

        tree = ET.parse(filename)
        root = tree.getroot()

        finalRoot = minidom.Document()
        finalXML = finalRoot.createElement('i3dMappings')
        finalRoot.appendChild(finalXML)

        sceneIndex = 0

        for i in root:
            if i.tag == 'Scene':
                break
            sceneIndex += 1

        scene = root[sceneIndex]

        rootIndex, lastLevel = 0, 0
        i3dStructure = {}
        index = []

        def getIndex(list, rootIndex, level=0):
            global index
            global lastLevel
            if len(list) >= 1:
                c = 0
                for i in list:
                    if lastLevel == level:
                        index = index[:-1]
                        index.append(c)
                    elif lastLevel > level:
                        temp = abs(lastLevel - level)
                        index = index[:-temp-1]
                        index.append(c)
                    else:
                        index.append(c)
                    indexBase = f'{rootIndex}>'
                    
                    if index:
                        for n in index:
                            indexBase += f'{n}|'
                    productChild = finalRoot.createElement('i3dMapping')
                    productChild.setAttribute('id',list[c].attrib['name'])
                    productChild.setAttribute('node',indexBase[:-1])
                    finalXML.appendChild(productChild)

                    lastLevel = level
                    c += 1
                    getIndex(i, rootIndex, level+1)

        for i in scene:
            productChild = finalRoot.createElement('i3dMapping')
            productChild.setAttribute('id',i.attrib['name'])
            productChild.setAttribute('node',f'{rootIndex}>')
            finalXML.appendChild(productChild)
            getIndex(i, rootIndex)
            rootIndex += 1

        xml_str = finalRoot.toprettyxml(indent ="\t")
        save_path_file = f'{filename[:-4]}_i3dMapping.xml'
        xml_str = xml_str.replace('&gt;','>')
        with open(save_path_file, 'w') as f:
            f.write(xml_str)

        print(f'File {file} completed and saved as {save_path_file}')
