import exifread 
import sys
import csv

def exif_read(file_location):
    # open image file
    f = open(file_location, 'rb')

    # Return exif tag
    tags = exifread.process_file(f)

    out_dic = {}

    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            #make dictionary
            out_dic[str(tag)] = str(tags[tag])

    with open("./output.csv", 'ab') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(list(out_dic.keys()))
        wr.writerow(list(out_dic.values()))
        
    f.close()

def main(file_location):
    exif_read(file_location)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Put python \"photo_analyze.py <Image location>\""
        sys.exit(1)
    
    file_location = sys.argv[1]

    print "File Location : %s" % file_location
    
    for n in sys.argv[1:]:
        print n
        main(n)

    #main(file_location)
    