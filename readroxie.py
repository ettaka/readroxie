def parse_version(roxiedata, content):
    section = ''
    for i,line in enumerate(content):
        splitline = line.replace('\n','').split()
        if 'VERSION' in line: 
            roxiedata['VERSION'] = splitline[1]
            return

def parse_cadata(roxiedata, content):
    section = ''
    for i,line in enumerate(content):
        splitline = line.replace('\n','').split()
        if '.cadata' in line: 
            roxiedata['cadata'] = splitline[0].replace("'",'')
            return

def parse_section(roxiedata, content, key, stopkey):
    section = ''
    for i,line in enumerate(content):
        splitline = line.replace('\n','').split()

        if not len(splitline) == 0:
            if key == splitline[0]: 
                section = key
                roxiedata[key] = []
                section_lines = []

        if section == key : 
            if stopkey in line:
                header_vars = splitline
                data = []
                for section_line in section_lines:
                    data.append({})
                    for i, header_var in enumerate(header_vars):
                        data[-1][header_var] = section_line[i]
                section = ''
                roxiedata[key] = data
            elif 'BLOCK' not in line:
                section_lines.append(splitline)




filename = 'TEST.data'
with open(filename) as f:
	content = f.readlines()

roxiedata = {}
parse_version(roxiedata, content)
parse_cadata(roxiedata, content)
parse_section(roxiedata, content, 'BLOCK', 'alpha')
parse_section(roxiedata, content, 'PLOT2D', 'zxaxis')

print roxiedata
