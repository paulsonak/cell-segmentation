'''
Batch download box folder
'''

import argparse
from boxsdk import Client, OAuth2
import os

parser = argparse.ArgumentParser(description='Downloads all files in a Box folder')
parser.add_argument('dev_token', type=str, help='Developer access token')
parser.add_argument('folder_id', type=str, help='Box.com folder id to download')
parser.add_argument('out_dir', type=str, help='output directory to save files')
parser.add_argument('--replace_flag', default=False, action='store_true', help='include flag if you want to overwrite files already on server')
args = parser.parse_args()

dev_token = args.dev_token
folder_id = args.folder_id
out_dir = args.out_dir
replace_flag=args.replace_flag

# Authorize client
oauth = OAuth2(
    client_id='4yskvwwpkcxqrjjcmfdpxw5aef3zqut0',
    client_secret='UnA76wItZzGh7FTyyoVxa1giajsoADCO',
    access_token=dev_token)
client = Client(oauth)

# Get list of files in folder

folder = client.folder(folder_id=folder_id).get()

# iterateFolder copies the files and file tree from box
# if replace_flag=True, files with same name will be overwritten
# if replace_flag=False, files with same name already on server won't be copied 
def iterateFolder(root_folder, root_folder_dir, replace_flag):
	files = root_folder.get_items(10000)
	for i in range(len(files)):
		f = files[i]
		if f._item_type=='folder':	
			fldname=f.name
			next_folder_dir=os.path.join(root_folder_dir, f.name)
			if not os.path.exists(next_folder_dir):
				os.makedirs(next_folder_dir)
			iterateFolder(client.folder(folder_id=f.object_id).get(), next_folder_dir, replace_flag=replace_flag)
		elif f._item_type=='file':
			file_name=os.path.join(root_folder_dir, f.name)
			if replace_flag==False:
				if os.path.exists(file_name)==True:
					print('Skipping ', f.name)
				else:
					print('Downloading ', f.name)
					with open(os.path.join(root_folder_dir, f.name), 'wb') as open_file:
						f.download_to(open_file)
			else:
				print('Downloading ', f.name)
				with open(os.path.join(root_folder_dir, f.name), 'wb') as open_file:
					f.download_to(open_file)
	return

iterateFolder(folder, out_dir, replace_flag)
print('Finished downloading.')

#movies folder: 41239774137
