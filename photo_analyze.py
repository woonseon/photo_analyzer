import exifread 
import sys
import csv
from PIL import Image

out_dic = {}
first_group = []
second_group = []
third_group = []

def exif_setting(file_location):
    # open image file
    f = open(file_location, 'rb')
    
    # out_dic initialize
    out_dic.clear()
    
    file_name = file_location.split('/')

    # Return exif tag
    tags = exifread.process_file(f)

    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            #make dictionary
            out_dic[str(tag)] = str(tags[tag])
    out_dic['file_name'] = file_name[2]

def exif_read(file_location):
    exif_setting(file_location)

    with open("./output.csv", 'ab') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(list(out_dic.keys()))
        wr.writerow(list(out_dic.values()))
        wr.writerow("")

def time():
    print "EXIF DateTimeOriginal" + out_dic['EXIF DateTimeOriginal']
    print "EXIF DateTimeDigitized" + out_dic['EXIF DateTimeDigitized']
    print "Image DateTime" + out_dic['Image DateTime']

def iso():
    print "EXIF ISOSpeedRatings " + out_dic['EXIF ISOSpeedRatings']

def gps():
    print "GPS: " + out_dic['GPS GPSLatitudeRef'],
    print out_dic['GPS GPSLatitude'],
    print out_dic['GPS GPSLongitudeRef'],
    print out_dic['GPS GPSLongitude'],
    print out_dic['GPS GPSAltitudeRef'],
    print out_dic['GPS GPSAltitude']

def extract():
    print "File name: " + out_dic['file_name']
    # Image Model
    print "========================================================"
    print "Image Model: " + out_dic['Image Model']
    # padding
    print "========================================================"
    try:
        print "Image padding: " + out_dic['Image Padding']
        print "EXIF padding: " + out_dic['EXIF Padding']
    except:
        print "Image padding: " + "none"
        print "EXIF padding: " + "none"
    
    # basic exif information
    # Image Exifoffset, EXIF InteroperabilityOffset, Thumbnail JPEGInterchangeFormat, EXIF ExifImageLength, EXIF ExifImageWidth
    print "Thumbnail JPEGInterchangeFormat: " + out_dic['Thumbnail JPEGInterchangeFormat']
    print "EXIF ExifImageLength: " + out_dic['EXIF ExifImageLength']
    print "Image Exifoffset: " + out_dic['Image ExifOffset']
    print "EXIF InteroperabilityOffset: " + out_dic['EXIF InteroperabilityOffset']
    print "Thumbnail JPEGInt: " + out_dic['EXIF ExifImageLength']
    print "EXIF ExifImageWidth: " + out_dic['EXIF ExifImageWidth']
    # Image DateTime
    print "========================================================"
    print "Image DateTime: " + out_dic['Image DateTime']
    # EXIF ShutterSpeedValue
    print "========================================================"
    print "EXIF ShutterSpeedValue: " + out_dic['EXIF ShutterSpeedValue']
    # Image Orientation
    print "========================================================"
    try:
        print "Image Orientation: " + out_dic['Image Orientation']
    except:
        print "Image Orientation: " + "none"
    print "========================================================"
    try:
        gps()
    except:
        print "GPS: none"
    print "========================================================"
    try:
        time()
    except:
        print "Time: none"
    print "========================================================"
    try:
        iso()
    except:
        print "ISO: none"
    print "========================================================\n"


def grouping(file_location):
    # size different
    open_image = Image.open(file_location)
    width, height = open_image.size

    #date different
    if ((out_dic['EXIF DateTimeOriginal'] != out_dic['EXIF DateTimeDigitized']) or (out_dic['EXIF DateTimeDigitized'] != out_dic['Image DateTime']) or (out_dic['Image DateTime'] != out_dic['EXIF DateTimeOriginal'])):
        first_group.append(out_dic['file_name'])
        #print "first group: " + out_dic['file_name']
    #size different
    elif (int(width) != int(out_dic['EXIF ExifImageWidth'])) or (int(height) != int(out_dic['EXIF ExifImageLength'])):
        second_group.append(out_dic['file_name'])
        #print "second group: " + out_dic['file_name']
    else:
        third_group.append(out_dic['file_name'])
        #print "thrid group: " + out_dic['file_name']

def select_menu():
    print "Select menu please"
    print "1. Extract EXIF Data for csv from Images"
    print "2. Print Important EXIF Data"
    print "3. Grouping Input Images"
    print "4. QUIT"
    selection = raw_input("Select menu : ")
    return selection

def main(file_location):
    exif_setting(file_location)

def main2(file_location):
    exif_read(file_location)

def main3(file_location):
    exif_setting(file_location)
    grouping(file_location)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Put \"python photo_analyze.py <Image location>\""
        sys.exit(1)

    while True:
        selec = select_menu()
        if selec is '1':
            for i in sys.argv[1:]:
                main2(i)
            print "Made output.csv!!!"
        elif selec is '2':
            for n in sys.argv[1:]:
                main(n)
                extract()
        elif selec is '3':
            for n in sys.argv[1:]:
                main3(n)
            print "Date Error Group: ",
            print first_group
            print "Size Error Group: ",
            print second_group
            print "Integrity Group: ",
            print third_group
            print ""
            
            # group init
            first_group = []
            second_group = []
            third_group = []
        else:
            print "Bye~"
            sys.exit()