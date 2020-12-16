class Cen:
    def clist():
        import re
        strings = []
        while True:
            cen = input()
            cen = re.sub(r'\s+', '+', cen)
            # replace~sym~>word
            cen = re.sub("[\^]", 's', cen)
            cen = re.sub("[\']", "'s+", cen)
            cen = re.sub("[#]", "'", cen)
            cen = re.sub("[\!]", "no+", cen)

            # rel_adv
            # when, where, what, how, why

            ramlist = ['(/[;])', '(/@)', '([/][~])', '(/_)', '([/][>])']
            rablist = ['/when+', '/where+', '/what+', '/how+', '/why+']

            for ram, rab in zip(ramlist, rablist):
                rac = re.compile(ram)
                cen = re.sub(rac, rab, cen)

            # split~sentence_#/#
            splist = []
            splcen = cen.split('/')

            for divcen in splcen:

                # rel_pron
                # what, which, who, whose, whom, that
                rpmlist = ['([*][=])', '([*][~])', '([*][-])', '([*][.])', '([*][_])', '[*]']
                rpblist = ['+what+', '+which+', '+who+', '+whose+', '+whom+', '+that+']

                for rpm, rpb in zip(rpmlist, rpblist):
                    rpc = re.compile(rpm)
                    divcen = re.sub(rpc, rpb, divcen)

                # [to, for, and, with, on, by, through, at, as, or, of, in, is]
                symlist = ["(~>)", '(>~)', '[&]', '[,][,]', '(_@)', '[_]', '(@~)', '@', r'[\\]', '[\|][\|]', '[.]',
                           '[$]', '[;]', '[\:]', '[=]']
                sublist = ['+to+', '+for+', '+and+', '+with+', '+on+', '+by+', '+through+', '+at+', '+as+', '+or+',
                           '+of+', '+in+', '+when+', '+if+', '+is+']

                for sym, sub in zip(symlist, sublist):
                    com = re.compile(sym)
                    divcen = re.sub(com, sub, divcen)

                # phrase
                divcen = re.sub('[+]', '`', divcen)
                divcen = re.sub('(-/)', '[+]', divcen)
                divcen = re.sub("[\(\)]", '/', divcen)
                ssplit = divcen.split('/')
                al = []
                for sp in ssplit:
                    if re.findall('-', sp) != []:
                        if re.findall('^-', sp) != []:
                            sp = re.sub('^-', '^', sp)
                        spl = sp.split('-')
                        spl.reverse()
                        sa = '`'.join(spl)
                        al.append(sa)
                    else:
                        al.append(sp)

                divcen = '`'.join(al)
                # phrase order
                divcen = re.sub('[+]', '-', divcen)
                ssplit2 = divcen.split('-')
                ssplit2.reverse()
                divcen = '`'.join(ssplit2)
                # sentence order
                divcen = re.sub(r'[\^]', '-', divcen)
                csplit = divcen.split('-')
                csplit.reverse()
                divcen = '`'.join(csplit)
                splist.append(divcen)
            cen = '`'.join(splist)

            cen = re.sub('~', '`', cen)
            cen = re.sub('`', ' ', cen)
            cen = re.sub('[\[]|[\]]', '', cen)
            cen = re.sub('\s+', ' ', cen)
            cen = cen.strip()
            cen = cen.capitalize()
            print(cen)
            if cen == '':
                break
            else:
                strings.append(cen)
        return strings

    def cdata(cen):
        import re
        import numpy as np
        import pandas as pd

        sbj = ''
        if re.findall('(<[\w\s]+>)', cen) != []:
            sbj = re.sub('[<>]', '', re.findall('(<[\w\s]+>)', cen)[0])

        cen = re.sub('(<[\w\s]+>)', '', cen)

        inc = []
        if re.findall('([\w\s]+;[{][\w\s,]+[}])', cen) !=[]:
            l_pinc = re.findall('([\w\s]+;[{][\w\s,]+[}])', cen)
            for pinc in l_pinc:
                key = re.sub(';', '', re.findall('([\w\s]+;)', pinc)[0])
                el_val = re.sub('[{}]', '', re.findall('([{][\w\s,]+[}])', pinc)[0]).split(',')
                inc.append({key:el_val})
            cen=re.sub('([\w\s]+;[{][\w\s,]+[}])','',cen)

        com = []
        if re.findall('([\[][\w\s,]+[\]][\[][\w\s\(\),\:]+[\]])', cen) != []:
            l_pcom = re.findall('([\[][\w\s,]+[\]][\[][\w\s\(\),\:]+[\]])', cen)
            for pcom in l_pcom:
                l_ind = re.sub('[\[\]]','',re.findall('([\[][\w\s,]+[\]])',pcom)[0]).split(',')
                d_com = pd.DataFrame(index=l_ind)
                l_sDat=[]
                l_mname = re.findall('([\w\s]+[\(])',pcom)
                l_name = []
                for mname in l_mname:
                    l_name.append(re.sub('[\(]','',mname))
                count = 0
                l_dat=[]
                while count<len(l_name):
                    l_dat.append(re.sub('[\(\)]', '', re.findall('[\(][\w\s,]+[\)]', pcom)[count]).split(','))
                    l_sDat.append(pd.Series(l_dat[count],name=l_name[count],index=l_ind))
                    count = count+1
                for sDat in l_sDat:
                    d_com=pd.concat([d_com, sDat], axis=1)
                print(d_com)
                com.append(d_com)
            cen = re.sub('([\[][\w\s,]+[\]][\[][\w\s\(\),\:]+[\]])','',cen)

        dat = []
        if re.findall('([\[][\w\s,]+[\]][\(][\w\s=\[\],]+[\)])',cen) !=[]:
            l_pdat = re.findall('([\[][\w\s,]+[\]][\(][\w\s=\[\],]+[\)])',cen)
            for pdat in l_pdat:
                l_col = re.sub('[\[\]]','',re.findall('([\[][\w\s,]+[\]])', pdat)[0]).split(',')
                l_mdata = re.findall('(=[\[][\w\s,]+[\]])', pdat)
                l_mdat=[]
                for mdata in l_mdata:
                    l_mdat.append(re.sub('=','',mdata))
                l_dat = []
                for mdat in l_mdat:
                    l_dat.append(re.sub('[\[\]]','',mdat).split(','))
                l_mind = re.findall('([\w\s]+=)',pdat)
                l_ind = []
                for mind in l_mind:
                    l_ind.append(re.sub('=','',mind))
                n_dat=np.array(l_dat)
                dat.append(pd.DataFrame(n_dat,columns=l_col,index=l_ind))
            cen=re.sub('([\[][\w\s,]+[\]][\(][\w\s=\[\],]+[\)])','',cen)

        rd = []
        if re.findall('([\(][\w\s\->]+[\)])',cen) !=[]:
            l_prd = re.findall('([\(][\w\s\->]+[\)])',cen)
            for prd in l_prd:
                count = 1
                l_dat = re.sub('[\(\)]','',prd).split('->')
                l_ind = []
                while count<=len(l_dat):
                    l_ind.append(count)
                    count = count+1
                rd.append(pd.Series(l_dat, index=l_ind))
            cen=re.sub('([\(][\w\s\->]+[\)])','',cen)

        par = []
        if re.findall('([\{][\w\s\:,]+[\}])',cen) !=[]:
            l_ppar = re.findall('([\{][\w\s\:,]+[\}])',cen)
            for ppar in l_ppar:
                l_mkey = re.findall('([\w\s]+\:)',ppar)
                l_key = []
                for mkey in l_mkey:
                    l_key.append(re.sub('[\:]','',mkey))
                l_mvar = re.findall('([\:][\w\s]+)',ppar)
                l_var = []
                for mvar in l_mvar:
                    l_var.append(re.sub('[\:]','',mvar))
                d_par = {}
                for key, var in zip(l_key,l_var):
                    d_par[key] = var
                par.append(pd.Series(d_par))
            cen=re.sub('([\{][\w\s\:,]+[\}])','',cen)

        li = []
        if re.findall('([\[][\w\s,]+[\]])',cen) !=[]:
            l_pli = re.findall('([\[][\w\s,]+[\]])',cen)
            for pli in l_pli:
                li.append(re.sub('[\[\]]','',pli).split(','))
            cen=re.sub('([\[][\w\s,]+[\]])','',cen)


        return {'sbj':sbj, 'li':li, 'ord':rd, 'inc':inc, 'com':com, 'dat':dat, 'par':par}



