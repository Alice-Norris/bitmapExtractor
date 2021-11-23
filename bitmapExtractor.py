import struct

class ico:
    fileName = ''
    #variable to hold whether file is an icon or cursor.
    #if it is 1, it is an icon. if it is 2, it is a cursor.
    icoType = 0
    imageCount = 0 #number of images in file
    #list of icon directory entries. Each entry is a list, in this order:
    #image width, image height, color count, color planes, bit count, image data size (bytes), image data offset
    iconDirectory = [] #list of icon directory entries.
    def __init__(self, fileName, icoType, imageNum):
        self.fileName = fileName
        if icoType == 1:
            self.icoType = 'Icon'
        if icoType == 2:
            self.icoType = 'Cursor'
        else:
            self.icoType = 'Corrupt'
    
        self.imageCount = imageNum




cursorDataReader =  open(file="bucket.cur", mode='rb+', buffering=0)


#data parsers for icon data
iconDirParser = struct.Struct("<3h")
iconDirEntryParser = struct.Struct("<4b 2h 2i")
bitmapInfoHeaderParser = struct.Struct("<3l 2h 6l")

#iconDirData = bytes(cursorDataReader.read(6)) #read six bytes, to be decoded by iconDirParser

iconDirectory = iconDirParser.unpack(bytes(cursorDataReader.read(6))) #set iconDirectory to a tuple containing image data
icon = ico(cursorDataReader.name, iconDirectory[1], iconDirectory[2]) #create new icon

while len(icon.iconDirectory) < icon.imageCount:
    iconDirEntry = ([*iconDirEntryParser.unpack(bytes(cursorDataReader.read(16)))])
    iconDirEntry.pop(3)
    icon.iconDirectory.append(iconDirEntry)


for imageNum, imageHeader in enumerate(icon.iconDirectory):
     print('Image Number: {0} of {1}'
        '\n\tFile Name:{2}'
        '\n\tFile Type: {3}'
        '\n\tWidth: {4}'
        '\n\tHeight: {5}'
        '\n\tColor Count: {6}'
        '\n\tPlanes: {7}'
        '\n\tBitCount: {8}'
        '\n\tImage Data Size In Bytes: {9}'
        '\n\tImage Data Offset: {10}'
        .format(imageNum+1, len(icon.iconDirectory), icon.fileName, icon.icoType, *imageHeader))

for pos, iconDirEntry in enumerate(icon.iconDirectory): #for each entry in the icon directory...
    cursorDataReader.seek(iconDirEntry[6]) #...seek to the address of the file where the image data is found
    #read info the size of the bitmapInfoHeader, unpack the result into a list, bitmapInfoHeader
    bitmapInfoHeader = [*bitmapInfoHeaderParser.unpack(bytes(cursorDataReader.read(40)))]
    bitmapInfoHeader.insert(5, bitmapInfoHeader[6])
    del(bitmapInfoHeader[6:])
    print('Bitmap Info for Image {0} of {1}:'
        '\n\tSize of header (bytes): {2}'
        '\n\tWidth (pixels): {3}'
        '\n\tHeight (pixels): {4}'
        '\n\tColor Planes: {5}'
        '\n\tBits per Pixel: {6}'
        '\n\tSize of Image (bytes): {7}'.format(pos, icon.imageCount, *bitmapInfoHeader))
    #add the bitmap info to the end of each directory entry.
    iconDirEntry.append(bitmapInfoHeader) 

