import pandas as pd

class NullData:
	def __init__(self, df:pd.DataFrame):
		self.df = df
		print('Automation in Action...!!!')
  
	def _fill_columns(self, fill_columns):
		if len(fill_columns) !=0 : return fill_columns
		else: return self.df.columns

	def fill_with_zero(self, fill_columns=[])->pd.DataFrame:
		fill_columns = self._fill_columns(fill_columns)
		for column in fill_columns:
			self.df[column].fillna(value=0, inplace=True)
		return self.df


	def fill_with_ffill(self, fill_columns)->pd.DataFrame:
		fill_columns = self._fill_columns(fill_columns)
		# fill null values with forward fill
		self.df.loc[:, fill_columns] = self.df.loc[:, fill_columns].ffill(axis='columns')	
		return self.df

	def fill_with_bfill(self, fill_columns)->pd.DataFrame:
		fill_columns = self._fill_columns(fill_columns)
		# fill null values with backward fill
		self.df.loc[:, fill_columns] = self.df.loc[:, fill_columns].bfill(axis='columns')	
		return self.df

	def fill_with_mean(self, fill_columns)->pd.DataFrame:
		fill_columns = self._fill_columns(fill_columns)
		# fill null values with mean
		for column in fill_columns:
			column_mean = self.df[column].mean()
			self.df[column].fillna(value=column_mean, inplace=True)
		return self.df

	def fill_with_mode(self, fill_columns)->pd.DataFrame:
		fill_columns = self._fill_columns(fill_columns)
		# fill null values with mode
		for column in fill_columns:
			column_mode = self.df[column].mode()[0]
			self.df[column].fillna(value=column_mode, inplace=True)
		return self.df

	def fill_with_median(self, fill_columns)->pd.DataFrame:
		fill_columns = self._fill_columns(fill_columns)
		# fill null values with mode
		for column in fill_columns:
			column_median = round(self.df[column].median(),1)
			self.df[column].fillna(value=column_median, inplace=True)
		return self.df

	def drop_rows(self, drop_in_columns=[])->pd.DataFrame:
		drop_in_columns = self._fill_columns(drop_in_columns)
		# drop rows for certain columns or all of them
		if drop_in_columns:
			self.df.dropna(subset=drop_in_columns, inplace=True)
		else:
			self.df.dropna(inplace=True)
		return self.df

	def drop_unwanted_column(self, unwanted_columns)->pd.DataFrame:
		# drop columns in the list unwanted_columns
		self.df.drop(unwanted_columns, axis=1, inplace=True)
		return self.df

	def drop_duplicate(self)->pd.DataFrame:
		# drop all duplicates
		self.df.drop_duplicates(inplace=True)
		return self.df

	def convert_to_datetime(self, datetime_columns)->pd.DataFrame:
		# convert a list of columns to datetime format
		for column in datetime_columns:
			self.df[column] = pd.to_datetime(self.df[column], format='%Y%m%d : %H%M%S')
		return self.df

	def treat_outliers_with_mode(self, fill_columns)->pd.DataFrame:
		# loop through columns
		# find min_threshol and max of column
		# replace max by mode, min by min
		for column in fill_columns:
			min_threshold, max_threshold = self.df[column].quantile([0.001,0.999])
			column_mode = self.df[column].mode()[0]
			column_min = self.df[column].min()
			# replacing ouliers
			self.df.loc[(self.df[column]>max_threshold),column] = column_mode
			self.df.loc[(self.df[column]<min_threshold),column] = column_min
		return self.df
