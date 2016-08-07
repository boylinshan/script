# -*- coding:utf-8 -*-
import sys
import os
import re
import argparse

class CNStringChecker(object):
	def __init__(self, input_path, output_path):
		#input_path:要检测的文件或文件夹的路径
		#output_path:检查结果输出的路径
		super(CNStringChecker, self).__init__()
		self.files_list = []
		self.check_path = None 
		self.output_path = os.path.abspath(output_path)

		self._re_expression = re.compile(r""".*["'].*["'].*""")
		self._on_long_commit = False
		self._long_commit_marks = ('"""', "'''")
		self._short_commit_marks = ('#')
		self._string_marks = ('"', "'")

		self._convert_path(os.path.abspath(input_path))

		#暂时写死
		self.ingoreList = ('E:\H48_SVN\code\client\script\client_data', 'E:\H48_SVN\code\client\script\game_common\data', 
						 	'E:\H48_SVN\code\hd2_server\server\engine\game_common\data')

		return

	def collectFiles(self, path, extend_type='.py'):
		#收集输入路径中的文件
		for dirpath, dirnames, filenames in os.walk(path):
			if dirpath.startswith(self.ingoreList):
				print dirpath
				continue
				
			for item in filenames:
				if item.lower().endswith(extend_type): 
					self.files_list.append(os.path.join(dirpath,item))

		return

	def checkCNString(self):
		#检查文件中的字符串
		if self.check_path:
			self.collectFiles(self.check_path)

		with open(self.output_path,'w') as output_file:
			for item in self.files_list:
				output = self._extractOneFile(item)

				if output:
					pos = len(self.check_path) if self.check_path else 0
					#print '\n{0}\n'.format(item[pos:])
					output_file.write('\n{0}\n'.format(item[pos:]))
					for info in output:
						#print info
						output_file.write(info)

		return

	def _convert_path(self, path):
		if os.path.isdir(path):
			self.check_path = path

		if os.path.isfile(path):
			self.files_list.append(path)

		return

	def _extractOneFile(self, cur_file):
		output = []
		self._on_long_commit = False
		with open(cur_file,'r') as f:
			context = f.readlines()
			for num in range(len(context)):
				line = self._clean_string(context[num])
				if self._re_expression.match(line) and self._check_contain_chinese(line):
					output.append('line:{0}\n'.format(num+1))

		return output

	def _clean_string(self, input_string):
		#过滤注释内容
		input_string = input_string.strip()

		if input_string in self._long_commit_marks:
			self._on_long_commit = not self._on_long_commit
			return ''

		if input_string[0:3] in self._long_commit_marks:
			if input_string[-3:] not in self._long_commit_marks:
				self._on_long_commit = True
			else:
				self._on_long_commit = False
			return ''

		if self._on_long_commit:
			return ''

		on_string = False
		mark_pos = 0
		for pos in range(len(input_string)):
			if input_string[pos] in self._string_marks:
				if not on_string:
					on_string = True
					mark_pos = pos
				elif input_string[mark_pos] == input_string[pos]:
					on_string = False

			if input_string[pos] in self._short_commit_marks and not on_string:
				input_string = input_string[0:pos]
				return input_string

		return input_string

	def _check_contain_chinese(self, line):
		try:
			for ch in line.decode('utf-8'):
				if u'\u4e00' <= ch <= u'\u9fff':
					return True
		except UnicodeDecodeError, e:
			#文件中有些无法decode的字符，暂无中文字符有此问题，所以暂时简单返回False
			return False

		return False

if __name__ == '__main__':
	tool = CNStringChecker(sys.argv[1], sys.argv[2])
	tool.checkCNString()


