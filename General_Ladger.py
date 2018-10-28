import pandas as pd
import numpy as np
pd.options.display.float_format = '{:,.0f}'.format
pd.options.display.max_rows = 200

class General_Ladger:
    def __init__(self, fn):
        self.fn = fn
        self.create_gl()
        #self.gl = gl
        #self.acc = acc
        #self.sub = sub
        #self.div = div
    

    def create_gl(self):
        """
        Convert Journal to GL.
        """
        gl0 = pd.read_csv(self.fn)
        gl1 = gl0.dropna(subset=['日付'])
        columns = ['日付',
                '伝票No.',
                '自勘定科目名', 
                '自補助科目名', 
                '自部門名', 
                '相手勘定科目名', 
                '相手補助科目名', 
                '税区分', 
                '摘要', 
                '借方金額', 
                '貸方金額'
                ]
        dr0 = gl1.loc[:,[
            '日付',
            '伝票No.', 
            '借方勘定科目', 
            '借方補助科目', 
            '借方部門', 
            '貸方勘定科目', 
            '貸方補助科目', 
            '摘要', 
            '借方税区分', 
            '借方金額', 
            '貸方金額'
            ]]
        cr0 = gl1.loc[:,[
            '日付', 
            '伝票No.', 
            '貸方勘定科目', 
            '貸方補助科目', 
            '貸方部門', 
            '借方勘定科目', 
            '借方補助科目', 
            '摘要', 
            '貸方税区分', 
            '借方金額', 
            '貸方金額'
            ]]

        dr0.loc[:,'貸方金額'] = 0
        cr0.loc[:,'借方金額'] = 0

        dr1 = dr0.rename(columns={
            '借方勘定科目': '自勘定科目名', 
            '借方補助科目': '自補助科目名', 
            '借方部門': '自部門名',
            '貸方勘定科目': '相手勘定科目名',
            '貸方補助科目': '相手補助科目名',
            '借方税区分': '税区分'
            })
        cr1 = cr0.rename(columns={
            '貸方勘定科目': '自勘定科目名',
            '貸方補助科目': '自補助科目名',
            '貸方部門': '自部門名',
            '借方勘定科目': '相手勘定科目名',
            '借方補助科目': '相手補助科目名',
            '貸方税区分': '税区分'
            })

        ttl0 = pd.concat([dr1, cr1])
        ttl1 = ttl0[columns]
        ttl2 = ttl1.dropna(subset=['自勘定科目名'])
        ttl3 = ttl2.sort_values(['日付', '伝票No.'])
        gl = ttl3.reset_index(drop=True)
        gl.loc[:,'残高'] = gl.apply(lambda x:(x['借方金額'] - x['貸方金額']),axis=1)
        return gl

    def search_gl(self, acc='', sub='', div=''):
        gl = self.create_gl()
        gl_acc = gl[gl['自勘定科目名'].str.contains(acc, na=False)]
        gl_acc_sub = gl_acc[gl_acc['自補助科目名'].str.contains(sub, na=False)]
        gl_acc_sub_div = gl_acc_sub[gl_acc_sub['自部門名'].str.contains(sub, na=False)]
        gl_acc_div = gl_acc[gl_acc['自部門名'].str.contains(div, na=False)]
        gl_sub = gl[gl['自補助科目名'].str.contains(sub, na=False)]
        gl_sub_div = gl_sub[gl_sub['自部門名'].str.contains(div, na=False)]
        gl_div = gl[gl['自部門名'].str.contains(div, na=False)]

        if len(acc) == 0 and len(sub) == 0 and len(div) == 0:
            return gl
        if len(acc) == 0 and len(sub) == 0:
            return gl_div
        if len(acc) == 0 and len(div) == 0:
            return gl_sub
        if len(sub) == 0 and len(div) == 0:
            return gl_acc
        if len(acc) == 0:
            return gl_sub_div
        if len(sub) == 0:
            return gl_acc_div
        if len(div) == 0:
            return gl_acc_sub