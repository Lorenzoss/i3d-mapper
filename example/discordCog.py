# This is an extension for a Discord bot. It waits for i3d files sent in a pre-determined channel,
# it downloads them, generate the i3d mapping and send the final XML to the user via DM.

import discord
import os
import asyncio
import requests
import xml.etree.ElementTree as ET
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from xml.dom import minidom

def checkDir(nameDir):
    if not os.path.exists(nameDir):
        os.mkdir(nameDir)

def getFile(linkFile, filename):
    r = requests.get(linkFile, stream=True)
    with open(filename, 'wb') as f:
        f.write(r.content)

index = []
lastLevel = 0
channelID = 111111111111111111  # To be replaced
guildID = 111111111111111111  # To be replaced

class I3Dmapping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        client = self.client
        if ctx.channel.id == channelID:
            if not ctx.author.bot:
                if ctx.attachments:
                    for attachment in ctx.attachments:
                        if (attachment.filename[-3:]) == 'i3d':
                            firstDate = datetime.today()
                            checkDir('temp/RawI3D')
                            checkDir('temp/i3dMappings')
                            RawI3D_fileName = f'temp/RawI3D/{attachment.filename}'
                            getFile(attachment.url, RawI3D_fileName)

                            await ctx.delete(delay=0)

                            tree = ET.parse(RawI3D_fileName)
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

                            rootIndex = 0

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

                                        productChild = finalRoot.createElement(
                                            'i3dMapping')
                                        productChild.setAttribute(
                                            'id', list[c].attrib['name'])
                                        productChild.setAttribute(
                                            'node', indexBase[:-1])
                                        finalXML.appendChild(productChild)

                                        lastLevel = level
                                        c += 1
                                        getIndex(i, rootIndex, level+1)

                            for i in scene:
                                productChild = finalRoot.createElement(
                                    'i3dMapping')
                                productChild.setAttribute(
                                    'id', i.attrib['name'])
                                productChild.setAttribute(
                                    'node', f'{rootIndex}>')
                                finalXML.appendChild(productChild)
                                getIndex(i, rootIndex)
                                rootIndex += 1

                            xml_str = finalRoot.toprettyxml(indent="\t")
                            save_path_file = f'temp/i3dMappings/{attachment.filename[:-4]}_i3dMapping.xml'
                            xml_str = xml_str.replace('&gt;', '>')
                            with open(save_path_file, 'w') as f:
                                f.write(xml_str)

                            secondDate = datetime.today()
                            time = secondDate - firstDate

                            file = discord.File(
                                save_path_file, filename=f'{attachment.filename[:-4]}_i3dMapping.xml')
                            member = client.get_guild(guildID).get_member(ctx.author.id)
                            dm = await member.create_dm()
                            await dm.send('', file=file)
                        else:
                            await ctx.delete()
                            break
                else:
                    await ctx.delete()

def setup(client):
    client.add_cog(I3Dmapping(client))
