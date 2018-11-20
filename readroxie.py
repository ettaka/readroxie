
filename = 'TEST.data'
with open(filename) as f:
	content = f.readlines()

roxiedata = {}
section = ''
for i,line in enumerate(content):
    splitline = line.replace('\n','').split()
    if 'VERSION' in line: roxiedata['VERSION'] = splitline[1]

    section_keys = ['BLOCK']
    for key in section_keys:
        if not len(splitline) == 0:
            if key == splitline[0]: 
                section = key
                roxiedata[key] = []
                section_lines = []
                break

    if section == 'BLOCK' : 
        if 'alpha' in line:
            header_vars = splitline
            data = []
            for section_line in section_lines:
                data.append({})
                for i, header_var in enumerate(header_vars):
                    data[-1][header_var] = section_line[i]
            section = ''
            roxiedata['BLOCK'] = data
        elif 'BLOCK' not in line:
            section_lines.append(splitline)


print roxiedata['BLOCK'][3]['radius']


