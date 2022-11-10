import os.path
import os
import csv
from flask import url_for
import zipfile

class ExportDataController:

    def file_is_existed(self, name):
        file_path = f'src/static/storage/audios/recordings/'+name
        return os.path.exists(file_path)
    
    def create_directory(self, directory_name):
        if not os.path.exists('src/static/exported/'+directory_name):
            os.mkdir('src/static/exported/'+directory_name)
        return 'src/static/exported/'+directory_name
    
    def create_csv_file(self, directory_name, filename, fieldList, itemList):
        directory = self.create_directory(directory_name=directory_name)
        with open(f'{directory}/{filename}.csv', 'w', newline='') as file:
            thewriter = csv.writer(file)
            thewriter.writerow(fieldList)
            number_of_col = len(fieldList)
            for col in itemList:
                item_col = []
                for index in range(0, number_of_col):
                    item_col.append(col[index])
                thewriter.writerow(item_col)
        return directory_name
    
    def create_zip_file(self, zipname, directory_name, filenames, csv_filename):
        path = f'src/static/storage/audios/recordings/'
        with zipfile.ZipFile(f'src/static/exported/{directory_name}/{zipname}', 'w') as my_zip:
            my_zip.write(f'src/static/exported/{directory_name}/{csv_filename}')
            for filename in filenames:
                my_zip.write(f'{path}{filename}')
        return zipname



