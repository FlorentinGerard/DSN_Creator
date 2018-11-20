import pandas as pd
import glob
from New.DsnType import BlockType, DataType, RubriqueType
from New.BlockConf import BlockConf


doc_folder = '././doc/'
dsn_cahier_technique = 'dsn_cahier_technique'
excel_extension = '.xlsx'
dsn_excel = glob.glob(doc_folder + dsn_cahier_technique + '*' + excel_extension)
assert len(dsn_excel) != 0, f'No excel file containing "{dsn_cahier_technique}" found in "{doc_folder}" folder'
assert len(
    dsn_excel) < 2, f'More than one excel file containing "{dsn_cahier_technique}" found in "{doc_folder}" folder'

dsn_excel = dsn_excel[0]
# print('\nExcel file found:')
# print('   ', dsn_excel, end='\n\n')

dsn_dfs = pd.read_excel(dsn_excel, sheet_name=None)


def print_data_frames(dfs, verbose=False):
    for (df_name, df) in dfs.items():
        if verbose:
            print(df_name + '_' * (100 - len(df_name)))
            print(df.head(5), '\n')
        else:
            print(f"{df_name:15}   [{str(df.columns)}]")


print_data_frames(dsn_dfs)

root = BlockType(id='DSN', name='DSN_Root', )
root.append('S10.G00.00', 'Envoi')
root.append('S20.G00.05', 'Déclaration')
root.append('S90.G00.90', "Total de l'envoi")

df_blocks = dsn_dfs['Blocks']
df_rubriques = dsn_dfs['Fields']
df_data_type = dsn_dfs['Data Types']

fd_blocks_index_mapping = {'Id': 'id', 'Name': 'name', 'ParentId': 'parent_id', 'lowerBound': 'lower_bound',
                           'upperBound': 'upper_bound', 'Description': 'description'}
for index, row in df_blocks.iterrows():
    args = {fd_blocks_index_mapping[key]: value for key, value in row.items()}
    BlockType.append_in_parent(**args)

fd_rubriques_index_mapping = {'Block Id': 'block_id', 'Id': 'id', 'Name': 'full_name', 'Description': 'description',
                              'DataType Id': 'data_type_id', 'Comment': 'name'}
for index, row in df_rubriques.iterrows():
    args = {fd_rubriques_index_mapping[key]: value for key, value in row.items()}
    BlockType.append_rubrique(**args)

fd_data_type_index_mapping = {'Id': 'id', 'Nature': 'nature', 'Regexp': 'regex',
                              'Lg Min': 'lg_min', 'Lg Max': 'lg_max', 'Values': 'values'}
for index, row in df_data_type.iterrows():
    args = {fd_data_type_index_mapping[key]: value for key, value in row.items()}
    DataType(**args)


MAX_LENGTH_BLOCK = max(len(i.name) for i in BlockType.ids.values())
[print('Block name max length:', MAX_LENGTH_BLOCK, i)
 for i in BlockType.ids.values() if len(i.name) == MAX_LENGTH_BLOCK]

MAX_LENGTH_RUBRIQUE = max(len(i.name) for i in RubriqueType.ids.values())
[print('Rubrique name max length:', MAX_LENGTH_RUBRIQUE, i)
 for i in RubriqueType.ids.values() if len(i.name) == MAX_LENGTH_RUBRIQUE]

MAX_DEPTH = max(BlockType.ids.values(), key=lambda i: i.depth).depth
[print('MAX_DEPTH:', i, MAX_DEPTH)
    for i in BlockType.ids.values() if i.depth == MAX_DEPTH]

# root.deep_print(print_rubriques=False)

bcr = BlockConf(root)
bvr = BlockValue(bcr)
bir = bvr[0]


def print_block_conf(bc):
    print(bc)
    for b in bc:
        print_block_conf(b)


def print_block_value(bc):
    print(bc)
    for i in bc:
        for sb in i:
            print_block_value(sb)


def print_bock_instance(bi):
    print(bi)
    for bv in bi:
        for sbi in bv:
            print_bock_instance(sbi)

#print_bock_instance(bir)
