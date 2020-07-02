from maya import cmds as c

# This is a basic function for renaming your maya assets to the UE4 standard naming convention
# Ensure you have already named your assets, and any extensions will be set.
# style guide can be found here: https://github.com/Allar/ue4-style-guide#s

PREFIXES = {
    "mesh": "S_",
    "joint": "J_",
    "light": "L_",
    "material": "M_",
    "camera": None

}

DEFAULT_PREFIX = "G_"

def rename(selection=False):
    """
    This function will rename your maya assets to the UE4 standard naming convention.
    Ensure you have already named your assets, and any extensions will be set.
    Style guide can be found here: https://github.com/Allar/ue4-style-guide#s
    Args:
        selection: Whether or not we use the current selection

    Returns:
        A list of all the objects we operated on
    """
    objects = c.ls(selection=selection, dag=True) #lists objects objects

    if selection and not objects:
        raise RuntimeError("Please select objects you wish to rename")

    objects.sort(key=len, reverse=True)

    for obj in objects:
# sources short name of objects base object
        shortName = obj.split("|")[-1]

        children = c.listRelatives(obj, children=True, fullPath=True) or []
        if len(children) == 1:
            child  = children[0]
            objType = c.objectType(child)

        else:
            objType = c.objectType(obj)

# sets extension for each object type

        prefix = PREFIXES.get(objType, DEFAULT_PREFIX)

        if not prefix:
            continue

        if obj.startswith(prefix): # prevents renaming an object twice
            continue

        newName = prefix + shortName # defines new object name
        c.rename(obj, newName) # renames object

        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

        print(obj)

    print("Renaming complete! Ryan just smiled a lil")
    return objects


class button(object):
    windowName = "UE4 Prefixer"

    def show(self):
        if c.window(self.windowName, query=True, exists=True):
            c.deleteUI(self.windowName)

        c.window(self.windowName)

        self.buildUI()

        c.showWindow()

    def buildUI(self):
        colum = c.columnLayout()

        c.text(label="Press the button to rename to UE4 Extension")

        c.button(label="Rename", command=self.rename)

    def rename(self, *args):
        rename()

