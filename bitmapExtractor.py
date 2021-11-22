import struct
cursorDataReader =  open(file="bucket.cur", mode='rb+', buffering=0)
cursorData = bytes(cursorDataReader.read(6))

byteDataParser = struct.Struct("<h")
iconDirEntryParser = struct.Struct("<4b 2h 2i")
headerData = [*byteDataParser.iter_unpack(cursorData)]
for pos, val in enumerate(headerData):
    item = headerData.pop(pos)
    headerData.insert(pos, item[0])
icoType = headerData[1]

if icoType == 1:
    icoType = '.ICO'
if icoType == 2:
    icoType = '.CUR'

imgCount = headerData[2]
iconDirEntries = []
while len(iconDirEntries) < imgCount:
    iconDirEntry = ([*iconDirEntryParser.unpack(bytes(cursorDataReader.read(16)))])
    iconDirEntry.pop(3)
    iconDirEntries.append(iconDirEntry)

for imageNum, imageHeader in enumerate(iconDirEntries):
    print(imageHeader)
    print("Image Number: {0}\n\tFile Type: {8}\n\tWidth: {1}\n\tHeight: {2}\n\tColor Count: {3}\n\tPlanes: {4}\n\tBitCount: {5}\n\tImage Data Size In Bytes: {6}\n\tImage Data Offset: {7}"
    .format(imageNum+1, *imageHeader, icoType))
