import srttranslatelocal.srttranslate as srttranslate
import os
import argparse

def srt_translate():
    # Path to the TSV file
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputf", help="input srt file")
    parser.add_argument("--fl", help="from language")
    parser.add_argument("--tl", help="to language")
    parser.add_argument("--outputf", help="output srt file")
    parser.parse_args()
    
    inputpath = args.inputf
    outputpath = args.outputf
    from_lang = args.fl
    to_lang = args.tol
    
    srttranslate.translate_srt(from_lang,to_lang, input_file, output_file)
	
# Defining main function
def main():
    srt_translate()

# Using the special variable 
# __name__
if __name__=="__main__":
    main()
