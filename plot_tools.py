import pandas as pd
import math
import numpy as np

class PlotTool():
	SIZE_PATCH = 5
	def __init__(self):
		pass
	def openCstTxt(self, file_path):
		data = pd.read_csv(file_path, skiprows=1)
		# 使用空格（\s）拆分字符串为两列
		split_data = data.iloc[:, 0].str.split(expand=True)

		# 将拆分后的数据转换为两个列表
		fre = split_data[0].tolist()
		s_parameters = split_data[1].tolist()
		return [float(i) for i in fre], [float(i) for i in s_parameters]

	def loadStructureParameters(self, file_path):
		matrices = []
		# 读取 CSV 文件中的数据
		data = pd.read_csv(file_path, header=None)
		for index, row in data.iterrows():
			# 将每行展平的数据还原为原始矩阵
			original_matrix = row.values.reshape((self.SIZE_PATCH, self.SIZE_PATCH))
			matrices.append(original_matrix)
		return matrices

	def plot_mirrored_matrix(self, matrix):
		mirrored_y = np.concatenate((matrix, np.flip(matrix, axis=0)), axis=0)
		mirrored_10x10 = np.concatenate((mirrored_y, np.flip(mirrored_y, axis=1)), axis=1)
		return mirrored_10x10

	def openCstTxtPair(self, folder_path, num):
		"""二氧化钒和铝特殊仿真，返回一对"""
		# 金属态S11,S21. 介质态S11,S21
		file_name_S11M = f'/S11output{num}_M.txt'
		file_name_S21M = f'/S21output{num}_M.txt'
		file_name_S11I = f'/S11output{num}_I.txt'
		file_name_S21I = f'/S21output{num}_I.txt'
		fre1_M, s11_M = self.openCstTxt(folder_path + file_name_S11M)
		fre2_M, s21_M = self.openCstTxt(folder_path + file_name_S21M)
		fre1_I, s11_I = self.openCstTxt(folder_path + file_name_S11I)
		fre2_I, s21_I = self.openCstTxt(folder_path + file_name_S21I)
		return fre1_M, s11_M, fre2_M, s21_M, fre1_I, s11_I, fre2_I, s21_I

	def calAbsorb(self, s11, s21):
		absorb = [1 - s11_ ** 2 - s21_ ** 2 for s11_, s21_ in zip(s11, s21)]
		return absorb

	def calTransmission(self, s_parameters, mode='linear'):
		if mode == 'dB':
			transmission = [20 * math.log10(s ** 2) for s in s_parameters]
			return transmission
		elif mode == 'linear':
			transmission = [s ** 2 for s in s_parameters]
			return transmission
if __name__ == '__main__':
	path = r"C:\Users\10146\Desktop\新建文件夹\generated_data_3th.csv"
	plot_tool = PlotTool()
	loaded_matrices = plot_tool.loadStructureParameters(path)
	for idx, matrix in enumerate(loaded_matrices[:5]):  # 只打印前 5 个矩阵
		print(f"Matrix {idx + 1}:\n{matrix}\n")