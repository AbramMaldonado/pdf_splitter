from config import App
import pypdf
from pypdf import PdfWriter, PdfReader 
from pypdf.errors import PdfReadError

from contextlib import nullcontext
import logging
import datetime 
import os

#Set Location Paths
pathname = os.path.join(os.path.dirname(__file__), App.config["file_location"])
splitpathname = os.path.join(os.path.dirname(__file__), App.config["file_location"], App.config["splitfilelocation"], App.config["file_name"])
isExist = os.path.exists(pathname)
print(isExist)
isExist = os.path.exists(splitpathname) 
print(isExist)

# Create and configure logger  
logfilename = os.path.join(os.path.dirname(__file__), App.logging['output_folder'], App.logging['log_name'] + datetime.datetime.today().strftime("%Y-%m-%d") + ".log")
logging.basicConfig(filename=logfilename,
                    format='%(asctime)s %(message)s',
                    filemode='a',
                    level=logging.DEBUG)
 
# Creating an object
logger = logging.getLogger("PyPDF") 

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

logger.info("======== New Invocation==================================") 

def pdf_validate(filename) : 
    try:
        pdf_reader = PdfReader(open(filename, "rb"))
        return pdf_reader
    except PdfReadError:
        logger.exception() 
        logger.error("PDF_VALIDATE : INVALID PDF ERROR\n\t{}".format(filename))   
    except Exception as e:
        logger.error(e)
        logger.error("PDF_VALIDATE : \n\tInvalid PDF File\n\t{}".format(filename))

        

def split_pdf_to_two(filename,page_number):
    pdf_reader = pdf_validate(filename)
    try:
        #Run this call only once, O = 1 (size of the file)
        logger.info('Reading File : {}'.format(filename))
        file_len = len(pdf_reader.pages) 
        logger.info('\tFinished Reading File : {} : Pages found'.format(file_len))

        assert page_number < file_len
        pdf_writer1 = PdfWriter()
        pdf_writer2 = PdfWriter()

        # O = 1 (size of the file)
        # File 1 Pages [0 - Page_Number]
        for page in range(page_number): 
            pdf_writer1.add_page(pdf_reader.pages[page])
        # File 2 Pages [Page_Number +1 => End of Document]
        for page in range(page_number,file_len):
            pdf_writer2.add_page(pdf_reader.pages[page])

        # O = 1
        # PDF File Writter
        with open("part1.pdf", 'wb') as file1:
            pdf_writer1.write(file1)

        with open("part2.pdf", 'wb') as file2:
            pdf_writer2.write(file2)

    except AssertionError as e:
        logger.error("SPLIT_PDF_TO_TWO: \n\tThe PDF you are cutting has less pages than you want to cut!")  
    except Exception as e:
        logger.error("SPLIT_PDF_TO_TWO() : \n\t{}".format(e))


def each_file() :

    for file in folders: 


        
## MAIN Function
def main():
    logger.info('-------- The Processing has been Started for filename : {}'.format(pathname))
    try:  
        split_pdf_to_two(pathname, App.config['split_page'])
    except Exception as ex:
        logger.error('MAIN() : \n\t{}'.format(ex))


    # jira_query_latest() 
    logger.info('-------- The Processing has been completed -------------------------------------------------------')

## Lets Start
if __name__ == "__main__":
    main()
