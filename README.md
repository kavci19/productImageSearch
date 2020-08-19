# productImageSearch

Searches a CSV file and scans each barcode in every row, searches for the product image associated with the barcode on Google, and downloads results 
in a folder named "Product_Images" in the present directory.



Note: this project uses the google-images-download module. To download the updated module, enter the following command in your terminal:

      pip install git+https://github.com/Joeclinton1/google-images-download.git
      
      
if you have pip installed on your computer, or

      git clone https://github.com/Joeclinton1/google-images-download.git
      cd google-images-download && sudo python setup.py install
      
otherwise.
