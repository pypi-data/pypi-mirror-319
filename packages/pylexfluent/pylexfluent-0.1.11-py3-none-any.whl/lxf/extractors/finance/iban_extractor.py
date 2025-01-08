
###################################################################

import logging
from lxf.settings import get_logging_level

logger = logging.getLogger('iban extractor')
fh = logging.FileHandler('./logs/iban_extractor.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
#################################################################


from lxf.ai.ocr.iban_ocr import do_IBAN_Ocr_from_pdf
from lxf.extractors.finance.ibans.iban_analyzer import IbanAnalyzer
from lxf.services.try_safe import try_safe_execute_async


async def extract_data(file_path:str,**kwargs)->str:
    """
    Extrait les données d'un iban 
    """

    if file_path==None: 
        logger.error("Extract Data: file_path ne peut pas etre None")
        return None
    result = await try_safe_execute_async(logger,do_IBAN_Ocr_from_pdf, path_filename=file_path)
    if result!=None :
        analyzer:IbanAnalyzer= IbanAnalyzer(result)
        return await try_safe_execute_async(logger,analyzer.do_analyze)
    return result