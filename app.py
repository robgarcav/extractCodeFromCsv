# Description: This is the main file of the project
# Author: Roberto García Ávila
# Date: 2023-01-29
# Version: 1.0
# License: MIT
# Usage: python app.py
# Purpose: This util will clone it's current project structure and will scan XML files to stract code snippets as Java files.
import os

# print current path
print("Current path: " + os.getcwd())

# print list of directories on current directory but avoid files and hidden directories
print("Directories on current path: " + str([x for x in os.listdir() if os.path.isdir(x) and not x.startswith('.')]))

# get a file path from param and get that file content
def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# extract content of Source tag from XML file
def extract_source_code(file_content):
    return file_content.split('<Source>')[1].split('</Source>')[0]

# remove surrounding CDATA box if exist
def remove_cdata_box(source_code):
    return source_code.replace('<![CDATA[', '').replace(']]>', '')


#¢print("Content of file: " + remove_cdata_box(extract_source_code(get_file_content('test/test.xml'))))

# clone directory structure without files from current directory to a new directory named 'output' and print the full path of the new directory
def clone_directory_structure():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if not dir.startswith('.'):
                os.makedirs(os.path.join('output', root, dir), exist_ok=True)
    print("New directory structure created on: " + os.path.join(os.getcwd(), 'output'))

clone_directory_structure()

# evaluate if a file is a XML file
def is_xml_file(file_name):
    return file_name.endswith('.xml')

# evaluate if xml file contains a Source tag
def has_source_tag(file_content):
    return '<Source>' in file_content

# evaluate if xml file contains a CDATA box 
def has_cdata_box(source_code):
    return '<![CDATA[' in source_code

# write a file on the parallel directory output with the same name and .java extension and remove empty lines from top and bottom of the file. write the file as UTF-8
def write_java_file(source_code, file_path):
    with open(os.path.join('output', file_path.replace('.xml', '.java')), 'w', encoding='utf-8') as file:
        file.write(source_code.strip())


# iterate over all files on current directory and subdirectories. Ignore hidden files and directories. Ignore files that are not XML files. Ignore XML files that don't have a Source tag. Ignore XML files that have a CDATA box. Write Java files on the parallel directory output with the same name and .java extension. Dont enter hidden directories. Dont iterate under hidden directories.
def iterate_over_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if not file.startswith('.'):
                file_path = os.path.join(root, file)
                if is_xml_file(file_path):
                    file_content = get_file_content(file_path)
                    if has_source_tag(file_content):
                        source_code = extract_source_code(file_content)
                        print("Source code: " + source_code)
                        if has_cdata_box(source_code):
                            source_code = remove_cdata_box(source_code)
                        print("Source code without CDATA box: " + source_code)
                        write_java_file(source_code, file_path)
        for dir in dirs:
            if dir.startswith('.'):
                dirs.remove(dir)

# main function
def main():
    print("Starting...")
    iterate_over_files()
    print("Done!")





main()
