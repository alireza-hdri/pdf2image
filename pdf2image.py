import os
import pypdfium2 as pdfium
import configparser

class pdf_to_image:
    def __init__(self, config_path):
        
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        # Genral config 
        main = self.config["main"]
        self.raw_pdf_files_path = main.get("raw_pdf_files_path")
        self.raw_pdf_exctracted_files_path = main.get("raw_pdf_exctracted_files_path")
        
    def list_raw_pdf_files(self):
        # List only .pdf files 
        return [
            f for f in os.listdir(self.raw_pdf_files_path)
            if os.path.isfile(os.path.join(self.raw_pdf_files_path, f))
            and f.lower().endswith(".pdf")
        ]
        
    def create_image_from_pdf(self):
        
        raw_pdf_list = self.list_raw_pdf_files()
        print(raw_pdf_list)
        
        # Ensure extracted dir is exists
        os.makedirs(self.raw_pdf_exctracted_files_path,exist_ok=True)
        for pdf_file in raw_pdf_list:
            pdf_dir_path = os.path.join(self.raw_pdf_exctracted_files_path, pdf_file)
            raw_pdf_complete_path = os.path.join(self.raw_pdf_files_path, pdf_file)
            
            # Load a document
            pdf = pdfium.PdfDocument(f"{raw_pdf_complete_path}")
            
            # Create pdf file path
            #os.makedirs(pdf_dir_path)
            
            # Loop over pages and render
            for i in range(len(pdf)):
                page = pdf[i]
                image = page.render(scale=4).to_pil()
                image.save(f"{self.raw_pdf_exctracted_files_path}/{pdf_file}_{i:03d}.jpg")
            
            print(f"processing file {pdf_file} finished")

if __name__ == "__main__":
    config_path="./config.ini"
    pdf_to_image = pdf_to_image(config_path)
    pdf_to_image.create_image_from_pdf()