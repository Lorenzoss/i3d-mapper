# i3d-mapper
Simple standalone i3d mapper for Farming Simulator mods in python.

# Usage
Download the python script *i3dMapper.py* and run with the files you want to map as parameters.
For example:
```cmd
python i3dMapper.py file1.i3d file2.i3d file3.i3d
```

Or you can implement it in another application, you can see an example [here](https://github.com/Lorenzoss/i3d-mapper/blob/main/example/discordCog.py) as an extension for a discord bot.


# Limits
At the moment it does not check if two or more nodes have the same names. In case the 3d scene has more than an object with the same name they should be renamed differently or it's needed to remove the ones in excess from the XML.
Also, it maps all the objects in the scene, which can cause an issue with large scenes or if you want to map only certain meshes.


# Contributions
Feel free to contribute, update or improve the code!
