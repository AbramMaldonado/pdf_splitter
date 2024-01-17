class App : 
    config = {
        'file_name' : "3440_K6XIBuC8225_CD_Output.pdf",
        'file_location' : "split",
        'splitfilelocation' : "split",
        'split_page' : 177566
    }
    logging = { 
        'output_folder' : "Logs",
        'log_name':"LoggingFile-"
    }

def ConfigMod(config_name, new_variable, logger):
    logger.info("ConfigModCalled")