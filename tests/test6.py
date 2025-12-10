from src.process_candidate_form import Form
# Test the objects of process_candidate_forms

def main():
    # caa = Form()
    # print(caa)
    # print(caa.__dict__)
    # print(vars(caa))

    cols = ('ca', 'caa', 'cca', 'cac', 'caac', 'cacc', 'ccaa', 'ccac')
    out = {col: Form() for col in cols}
    # print(out['caa'])

    out['caa'].form = 'kai'
    out['caa'].priority += 5

    print(out['caa'])
    print(out['caa'].priority)
