import csv
import os
import filecmp
import shutil
from pathlib import Path


def parse_csvs(path, dstPath):
    collections = {}
    collection_images = {}
    adobe_images = {}
    library_files = {}
    library_folders = {}
    library_roots = {}
    with open(csvPath + 'AgLibraryCollection.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            collections[row['id_local']] = row
    with open(csvPath + 'Adobe_images.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            adobe_images[row['id_local']] = row
    with open(csvPath + 'AgLibraryFile.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            library_files[row['id_local']] = row
    with open(csvPath + 'AgLibraryFolder.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            library_folders[row['id_local']] = row
    with open(csvPath + 'AgLibraryRootFolder.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            library_roots[row['id_local']] = row
    with open(csvPath + 'AgLibraryCollectionImage.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            collection_images[row['id_local']] = row

    for id, image in collection_images.items():
        temp = {}
        collPath = resolve_collection_path(collections[image['collection']], collections, '')
        srcPath = resolve_source_path(adobe_images[image['image']], library_files, library_folders, library_roots)
        outPath = dstPath + collPath + resolve_source_name(adobe_images[image['image']], library_files)
        image['srcPath'] = Path(srcPath)
        image['dstPath'] = Path(outPath)

    for id, image in collection_images.items():
        print('-----')
        print('Source File: ' + str(image['srcPath']))
        print('  Dest File: ' + str(image['dstPath']))
        if not os.path.exists(image['dstPath']) or not filecmp.cmp(image['srcPath'], image['dstPath']):
            print('             COPYING... ', end='')
            if not os.path.exists(image['dstPath'].parent):
                os.makedirs(image['dstPath'].parent, exist_ok=True)
            shutil.copyfile(image['srcPath'], image['dstPath'])
            print('DONE!')
        else:
            print('             EXISTS, SKIPPING...')
    print()

def resolve_collection_path(collection, collections, path):
    if collection['parent'] == '':
        return collection['name'] + '/' + path
    return resolve_collection_path(collections[collection['parent']], collections, collection['name'] + '/' + path)

def resolve_source_path(image, files, folders, roots):
    file = files[image['rootFile']]
    folder = folders[file['folder']]
    root = roots[folder['rootFolder']]
    return root['absolutePath'] + folder['pathFromRoot'] + file['idx_filename']

def resolve_source_name(image, files):
    file = files[image['rootFile']]
    return file['idx_filename']


if __name__ == "__main__":
    csvPath = 'D:\\Lightroom CSVs\\'
    dstPath = 'E:\\PicturesMigrated\\'
    parse_csvs(csvPath, dstPath)