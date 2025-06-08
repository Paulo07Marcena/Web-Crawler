import pandas as pd

class processData():
    print('Process data init!')

    df = pd.read_csv('files/converted_file.csv', encoding='latin1', header=4)

    df_limpo = df.iloc[:, [0, 1]].copy()

    df_limpo.columns = ['Mês-Ano', 'Emplacamentos']

    df_limpo.loc[:, 'Emplacamentos'] = df_limpo['Emplacamentos'].astype(str).str.replace('.', '', regex=False)
    df_limpo.loc[:, 'Emplacamentos'] = df_limpo['Emplacamentos'].str.replace(',', '', regex=False)
    df_limpo.loc[:, 'Emplacamentos'] = pd.to_numeric(df_limpo['Emplacamentos'], errors='coerce')

    df_limpo = df_limpo[df_limpo['Emplacamentos'].notna()]

    df_limpo.to_csv('files/processed_file.csv', index=False, encoding='utf-8-sig')

    print('Process finished! Saved processed_file.csv')