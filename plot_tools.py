import os

import pandas as pd
import math
import lmdb
import pickle
import numpy as np
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QFileDialog
from scipy.interpolate import interp1d

class PlotTool(QThread):
	SIZE_PATCH = 5
	process_signal = Signal(int)
	finished_signal = Signal()
	def __init__(self):
		super().__init__()
		file_name_base_S11 = rf"C:\Users\10146\Desktop\BandStop\S11(5umbase).txt"
		file_name_base_S21 = rf"C:\Users\10146\Desktop\BandStop\S21(5umbase).txt"
		self.base_fre1, self.base_S11 = self.openCstTxt(file_name_base_S11)
		self.base_fre1, self.base_S11 = self.resample_data(self.base_fre1, self.base_S11)
		self.base_fre2, self.base_S21 = self.openCstTxt(file_name_base_S21)
		self.base_fre2, self.base_S21 = self.resample_data(self.base_fre2, self.base_S21)


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
		mirrored_y = np.concatenate((np.flip(matrix, axis=0), matrix), axis=0)
		mirrored_10x10 = np.concatenate((np.flip(mirrored_y, axis=1), mirrored_y), axis=1)
		return mirrored_10x10

	def resample_data(self, x, y, num_points=1001, kind='linear'):
		# 生成等间距的 x 值
		x_new = np.linspace(np.min(x), np.max(x), num_points)
		# 创建插值函数
		f = interp1d(x, y, kind=kind)
		# 计算新的 y 值
		y_new = f(x_new)
		return x_new, y_new

	def openCstTxtPair(self, folder_path, num):
		"""二氧化钒和铝特殊仿真，返回一对"""
		# 金属态S11,S21. 介质态S11,S21
		file_name_S11M = f'/S11output{num}_M.txt'
		file_name_S21M = f'/S21output{num}_M.txt'
		file_name_S11I = f'/S11output{num}_I.txt'
		file_name_S21I = f'/S21output{num}_I.txt'

		fre1_M, s11_M = self.openCstTxt(folder_path + file_name_S11M)
		fre1_M, s11_M = self.resample_data(fre1_M, s11_M)
		fre2_M, s21_M = self.openCstTxt(folder_path + file_name_S21M)
		fre2_M, s21_M = self.resample_data(fre2_M, s21_M)
		fre1_I, s11_I = self.openCstTxt(folder_path + file_name_S11I)
		fre1_I, s11_I = self.resample_data(fre1_I, s11_I)
		fre2_I, s21_I = self.openCstTxt(folder_path + file_name_S21I)
		fre2_I, s21_I = self.resample_data(fre2_I, s21_I)
		return fre1_M, s11_M, fre2_M, s21_M, fre1_I, s11_I, fre2_I, s21_I

	def calAbsorb(self, s11, s21):
		# s21 = s21 / self.base_S21
		absorb = [1 - s11_ ** 2 - s21_ ** 2 for s11_, s21_ in zip(s11, s21)]
		return absorb

	def calTransmission(self, s_parameters, mode='linear'):
		# s_parameters = s_parameters / self.base_S21
		if mode == 'dB':
			transmission = [20 * math.log10(s ** 2) for s in s_parameters]
			return transmission
		elif mode == 'linear':
			transmission = [s ** 2 for s in s_parameters]
			return transmission


	def saveAllLMDB(self, result_path, save_path, input_csv):
		# 打开一个 LMDB 数据库
		env = lmdb.open(save_path, map_size=1 * 1024 * 1024 * 1024)
		all_items = os.listdir(result_path)
		fils_num = len(all_items) / 4
		for i in range(int(fils_num)):
			self.process_signal.emit(i/int(fils_num) * 100 + 1)
			fre1_M, s11_M, fre2_M, s21_M, fre1_I, s11_I, fre2_I, s21_I = self.openCstTxtPair(result_path, i)
			matrix = self.plot_mirrored_matrix(input_csv[i])
			flattened_matrix = np.array(matrix).flatten()
			self.saveLMDBOne(env, f"data_{i}", flattened_matrix, self.calTransmission(s21_I, 'dB') + self.calTransmission(s21_M, 'dB'))
		self.finished_signal.emit()
	def saveLMDBOne(self, env, save_name, input_data, output_data):
		data_to_save = (input_data, output_data)
		# 开始一个写事务
		with env.begin(write=True) as txn:
			# 生成唯一键
			key = f'{save_name}'.encode('ascii')
			# 将数据序列化为字节流
			data_bytes = pickle.dumps(data_to_save)
			# 写入 LMDB
			txn.put(key, data_bytes)


class SaveLMDB(PlotTool):
	def __init__(self, cst_result_folder_path, save_path, cst_structure_parameters):
		super().__init__()
		self.cst_result_folder_path = cst_result_folder_path
		self.cst_structure_parameters = cst_structure_parameters
		self.save_path = save_path
	def run(self):
		self.saveAllLMDB(self.cst_result_folder_path, self.save_path, self.cst_structure_parameters)

if __name__ == '__main__':
	path = r"C:\Users\10146\Desktop\新建文件夹\generated_data_3th.csv"
	plot_tool = PlotTool()
	loaded_matrices = plot_tool.loadStructureParameters(path)
	for idx, matrix in enumerate(loaded_matrices[:5]):  # 只打印前 5 个矩阵
		print(f"Matrix {idx + 1}:\n{matrix}\n")