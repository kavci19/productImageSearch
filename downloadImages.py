import os
import sys
from google_images_download import google_images_download
import csv

from numpy.core.defchararray import rfind

response = google_images_download.googleimagesdownload()

unmatched_products = []

SAVE_FOLDER = 'Product_Images'
POSSIBLE_FOLDER = 'Possible_Matches'

def main():

    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    if not os.path.exists(POSSIBLE_FOLDER):
        os.mkdir(POSSIBLE_FOLDER)

    scan_barcodes()


def scan_barcodes():

    with open('BarcodesSheet.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            print()

            if line_count < 5716:
                line_count += 1
                continue

            else:

                progress = (line_count/20000)*100

                print(str(round(progress,2)) + '% done')

                barcode = row[1]
                name = row[0]
                
                download_image(barcode, name)

            line_count += 1

        print('Processed ' + str(line_count) + ' lines')
        print('Done')
        print()
        writeUnmatchedProducts()
        print('Could not find images for ' + str(len(unmatched_products)) + ' queries. See Unmatched_Products CSV file for details.')




def download_image(barcode, name):
    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")

    blockPrint()

    if "+" in barcode or "-" in barcode:
        try_download(barcode, name)
        return

    GOOGLE_IMAGE = \
        'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

    searchurl = GOOGLE_IMAGE + 'q=' + barcode

    arguments = {"keywords": barcode,
                 "format": "jpg",
                 "limit": 1,
                 "print_urls": True,
                 "size": "large",
                 "aspect_ratio": "panoramic",
                 "output_directory": SAVE_FOLDER,
                 "no_directory": True,
                 "url": searchurl,
                 "name": barcode}

    try:

        a = response.download(arguments)
        a = list(a[0].values())[0][0]
        lastIndex = a.rfind('\\')
        base = a[:lastIndex+1]
        newName = base + str(barcode) + '.jpg'
        os.rename(a, newName)
        enablePrint()

    except SystemExit:
        try:
            try_download(barcode, name)
        except:
            enablePrint()
            return
        enablePrint()
        return

    except IndexError:
        try:
            try_download(barcode, name)
        except:
            enablePrint()
            return
        enablePrint()
        return

    except FileExistsError:
        try:
            try_download(barcode, name)
        except:
            enablePrint()
            return
        enablePrint()
        return

    except FileNotFoundError:
        try:
            try_download(barcode, name)
        except:
            enablePrint()
            return
        enablePrint()
        return

    except OSError:
        try:
            try_download(barcode, name)
        except:
            enablePrint()
            return
        enablePrint()
        return





def try_download(barcode, name):

    GOOGLE_IMAGE = \
        'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

    searchurl = GOOGLE_IMAGE + 'q=' + name

    arguments = {"keywords": name,
                 "format": "jpg",
                 "limit": 1,
                 "print_urls": True,
                 "size": "large",
                 "aspect_ratio": "panoramic",
                 "output_directory": POSSIBLE_FOLDER,
                 "no_directory": True,
                 "url": searchurl,
                 "name": name}

    try:

        a = response.download(arguments)
        a = list(a[0].values())[0][0]
        lastIndex = a.rfind('\\')
        base = a[:lastIndex+1]
        newName = base + str(barcode) + '.jpg'
        os.rename(a, newName)

    except SystemExit:
        unmatched_products.append([name,barcode])
        return

    except IndexError:
        unmatched_products.append([name,barcode])
        return

    except FileExistsError:
        unmatched_products.append([name,barcode])
        return

    except FileNotFoundError:
        unmatched_products.append([name,barcode])
        return
    except OSError:
        return



# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def writeUnmatchedProducts():

    with open('Unmatched_Products.csv', mode='w') as unmatched:
        writer = csv.writer(unmatched, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for product in unmatched_products:
            writer.writerow(product)



if __name__ == '__main__':
    main()