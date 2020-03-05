"""Pre-process the pdfs from the unwcc.org site"""
import os
import PyPDF2


def pre_process_pdf(lb, ub, file, file_number, country, second_set=False, lb2=None, ub2=None):
    """Takes original pdf from unwcc.org site and removes unneccessary
    pages.
    
    Args:
        lb (non-negative integer): lower bound of pages to delete
        ub (non-negative integer): upper bound of pages to delete
        file (string): file name with extension
        file_number (non-negative integer): file number corresponds to pdf order
        second_set (Boolean): If True, it means you'd like to delete a second
        set of pages
        country (string): either american or british 
        lb2 (non-negative integer): for second set, lower bound of pages to delete
        ub2 (non-negative integer): for second set, upper bound of pages to delete
    Returns:
        Generates new file in folder location. Location restricted.
    
    """
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\{}".format(country))
    pages_to_delete = list(range(lb, ub)) # page numbering starts from 0
    if second_set:
        pages_to_delete.extend(list(range(lb2, ub2)))        
    war_infile = PyPDF2.PdfFileReader(r"{}".format(file), 'rb')
    war_pdf = PyPDF2.PdfFileWriter()

    # Extract all pages not in the pages to delete
    for i in range(war_infile.getNumPages()):
        if i not in pages_to_delete:
            p = war_infile.getPage(i)
            war_pdf.addPage(p)

    # Make pdf
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\{}\pre_processed_pdfs".format(country))
    with open('new_war_{}{}.pdf'.format(country, file_number), 'wb') as war:
        war_pdf.write(war)     
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder")


def pre_process_pdf2(pages_to_delete, file, file_number, country):
    """Takes original pdf from unwcc.org site and removes unneccessary
    pages.
    
    Args:
        pages_to_delete (list): list of page numbers to delete
        file (string): file name with extension
        file_number (non-negative integer): file number corresponds to pdf order
    Returns:
        Generates new file in folder location. Location restricted.
    
    """
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\{}".format(country))     
    war_infile = PyPDF2.PdfFileReader(r"{}".format(file), 'rb')
    war_pdf = PyPDF2.PdfFileWriter()

    # Extract all pages not in the pages to delete
    for i in range(war_infile.getNumPages()):
        if i not in pages_to_delete:
            p = war_infile.getPage(i)
            war_pdf.addPage(p)

    # Make pdf
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\{}\pre_processed_pdfs".format(country))
    with open('new_war_{}{}.pdf'.format(country, file_number), 'wb') as war:
        war_pdf.write(war)     
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder")