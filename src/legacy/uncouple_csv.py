import pandas as pd

def uncouple_csv(csv_in, cols, fp_out=None, delim='-', action='to_file'):

    df = pd.read_csv(csv_in, sep='\t', header=0)

    df = df.assign(
        **{col: df[col].str.split(delim) for col in cols}
        ).explode(cols).reset_index(drop=True)

    csv_text = df.to_csv()

    if fp_out is not None:
        with open(fp_out, 'w', encoding='utf-8', newline='\n') as f:
            f.write(csv_text)

    return csv_text