import config.threshholds as th
import src.lojban_specific.lpos as lpos
import src.newlang_specific.sound_changes as sound_changes
import src.lojban_specific.phonological_inventory as inv

class Row:

    def __init__(self, d: dict):
        self.rowdata = d
        self.override = d['override']
        self.gismu = d['gismu']
        self.gismu_shape = d['gismu_shape']
        self.pos_tendency = d['pos_tendency']

        self.freq_prefix = d['as_rafsi_im']
        self.freq_suffix = d['as_rafsi_fm']
        self._ri = d['%_ri']
        self._rf = d['%_rf']
        self._cmavo = d['%_cmavo']

        n1, n2 = d['coef1_1'], d['coef1_2']
        self.coef2 = round(n2 / n1 , 1) if n1 else 999

        if self.gismu:

            # Admit second forms if certain criteria met
            x = d['cmavo_rafsi_1'], d['form_shape_1'], d['rafsi_pos_1']
            y = d['cmavo_rafsi_2'], d['form_shape_2'], d['rafsi_pos_2']

            if (self.coef2 > th.coef_flip_threshhold
                and d['form_shape_1'] == 'CAA' and d['form_shape_2'] != 'CAA'):
                self.form1, self.shape1, self.pos1 = y
                self.form2, self.shape2, self.pos2 = x
            else:
                self.form1, self.shape1, self.pos1 = x
                self.form2, self.shape2, self.pos2 = y

            self.form1 = self.form1.replace("'", '')
            self.form2 = self.form2.replace("'", '')

            if not self.form1:
                self.pos_tendency = 'neut'
            
            self.gismu_type = self.gismu_shape[:2]

            # Normalise pos
            pos_dict = {'132': '134',
                    '231': '234',
                    '342': '345', '145': '345', '142': '345',
                    }
            self.pos1 = pos_dict.get(self.pos1, self.pos1)
            self.pos2 = pos_dict.get(self.pos2, self.pos2)

    @property
    def params1(self):
        return (self.gismu_type, self.poss)

    @property
    def diphthong_reduced(self):
        g = self.gismu
        aa = lpos.rearrange_by_lpos(g, 'AA 12')
        return sound_changes.diphthongs.get(aa, aa)

    def c1c2(self):
        cc = ''
        g = self.gismu
        if self.gismu_type == 'CC':    cc =  g[:2]
        elif self.gismu_type == 'CA':    cc = f'{g[0]}{g[2]}'
        return cc

    def get_other_rafsi(self):
        d = self.rowdata
        return ( d['cmavo_rafsi_1'], d['cmavo_rafsi_2'], d['cmavo_rafsi_3'], 
        *d['excluded_a'].split(' '), 
        *d['excluded_b'].split(' ') )

    def get_other_coda(self):
        rafsis = tuple((form for form in self.get_other_rafsi() if form))
        codas = tuple((char 
                        for char in (form[-1] for form in rafsis)
                        if char in inv.C
                        ))

        if len(codas) > 1:  print(rafsis)
        coda = codas[0] if codas else None
        return coda

    def find_in_shape(self, s):
        if s in self.gismu_shape:
            return self.gismu_shape.index(s)
        else:
            return -1
