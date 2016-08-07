import sys
import os
import re

files_list = []
class_inherit_dic = {}

def collectFiles(path, extend_type):
	files = []
	for dirpath, dirnames, filenames in os.walk(path):
		for item in filenames:
			name = item[item.rfind('.')+1:]
			if name == extend_type:
				files.append(os.path.join(dirpath,item))

	return files

def extractOneFile(path):
	with open(path,'r') as f:
		context = f.readlines()
		for line in context:
			line = line.strip()
			if re.match('class\s+\w+\s*\((\w+,\s*){0,}\w+\):', line):
				#This line is the name of class
				class_name = line[line.find(' '):line.find('(')].lstrip()
				base_class_list = line[line.rfind('(')+1:line.rfind(')')].split(',')

				for base in base_class_list:
					base = base.strip()
					if base not in class_inherit_dic:
						class_inherit_dic[base] = list()
						class_inherit_dic[base].append(class_name)
					else:
						class_inherit_dic[base].append(class_name)
	return

def organize(name, lv, f):
	if name not in class_inherit_dic:
		return

	base_class_list = class_inherit_dic[name]
	for base_class in base_class_list:
		if not lv:
			f.write('\n******BASE CLASS******\n')

		f.write('--'*lv + '{0}\n'.format(base_class))
		organize(base_class,lv+1,f)

	return

if __name__ == '__main__':
	cur_dir = sys.argv[1]
	files_list= collectFiles(cur_dir, 'py')

	for f in files_list:
		extractOneFile(f)

	with open(sys.argv[2], 'w') as f:
		organize('object', 0, f)


