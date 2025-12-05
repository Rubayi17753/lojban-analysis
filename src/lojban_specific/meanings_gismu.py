from src.tools.class_table import Table

def get_df_gismu_meaning(dfg=Table('defs_gismu').dff):
    # Handles meanings of the format wood ‘lumber’
	dfg['meaning'] = dfg['meaning'].str[1:-1]
	dfg[['meaning', 'mnemonic']] = dfg['meaning'].str.split(' ‘', n=1, expand=True)
	dfg['mnemonic'] = dfg['meaning'].str[:-1]
	return dfg