def parse_version(roxiedata, content):
    section = ''
    for i,line in enumerate(content):
        splitline = line.replace('\n','').split()
        if 'VERSION' in line: 
            roxiedata['VERSION'] = splitline[1]
            return

def parse_cadata_filepath(roxiedata, content):
    section = ''
    for i,line in enumerate(content):
        splitline = line.replace('\n','').split()
        if '.cadata' in line: 
            roxiedata['cadata'] = {}
            roxiedata['cadata']['filepath'] = splitline[0].replace("'",'')
            return

def stopkeys_in_line(line, stopkeys):
    for stopkey in stopkeys:
        if not stopkey in line: return False
    return True

def parse_section(roxiedata, content, key, stopkeys):
    section = ''
    for i,line in enumerate(content):
        splitline = line.replace('\n','').replace('/','').split()
        if not len(splitline) == 0:
            if key == splitline[0]: 
                if len(splitline) >=2 and splitline[1] == '0':
                    roxiedata[key] = []
                    return
                section = key
                roxiedata[key] = []
                section_lines = []

        if section == key: 
            if stopkeys_in_line(line, stopkeys):
                header_vars = splitline
                data = []
                for section_line in section_lines:
                    data.append({})
                    for i, header_var in enumerate(header_vars):
                        data[-1][header_var] = section_line[i]
                section = ''
                roxiedata[key] = data
            elif key not in line:
                section_lines.append(splitline)

def parse_roxiefile(filepath):
    with open(filepath) as f:
            content = f.readlines()

    roxiedata = {}
    parse_version(roxiedata, content)
    parse_cadata_filepath(roxiedata, content)
    parse_section(roxiedata, content, 'BLOCK', ['type', 'phi', 'current', 'alpha'])
    parse_section(roxiedata, content, 'PLOT2D', ['zxaxis'])

    with open(roxiedata['cadata']['filepath']) as f:
            cadata_content = f.readlines()


    parse_version(roxiedata['cadata'], cadata_content)
    parse_section(roxiedata['cadata'], cadata_content, 'CABLE', ['No','height','width_o'])
    return roxiedata

def test_parse_roxiefile():
    roxiedata = parse_roxiefile('TEST.data')
    print roxiedata['BLOCK']
    print roxiedata['PLOT2D']
    print roxiedata['cadata']


if __name__ == '__main__':
    test_parse_roxiefile()



