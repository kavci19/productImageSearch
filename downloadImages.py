import os
from google_images_download import google_images_download
import csv

from numpy.core.defchararray import rfind

response = google_images_download.googleimagesdownload()

SAVE_FOLDER = 'Product_Images'


def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    scan_barcodes()


def scan_barcodes():

    with open('BarcodesSheet.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:

            if line_count == 0:
                line_count += 1
                continue
            else:
                print("Scanning Item: " + str(line_count - 1))
                barcode = row[1]
                
                download_image(barcode)
                line_count += 1

        print('Processed ' + str(line_count) + ' lines')
        print('Done')



def download_image(query):
    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")

    if "+" in query or "-" in query:
        return

    GOOGLE_IMAGE = \
        'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

    searchurl = GOOGLE_IMAGE + 'q=' + query

    arguments = {"keywords": query,
                 "format": "jpg",
                 "limit": 1,
                 "print_urls": True,
                 "size": "large",
                 "aspect_ratio": "panoramic",
                 "output_directory": SAVE_FOLDER,
                 "no_directory": True,
                 "url": searchurl,
                 "name": query}

    try:

        a = response.download(arguments)
        a = list(a[0].values())[0][0]
        lastIndex = a.rfind('\\')
        base = a[:lastIndex+1]
        newName = base + str(query) + '.jpg'
        os.rename(a, newName)

    except SystemExit:
        return

    except IndexError:
        return

    except FileExistsError:
        return

    except FileNotFoundError:
        return





if __name__ == '__main__':
    main()