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

def parse_roxiefile(directory, filepath):
    with open(directory + '/' + filepath) as f:
            content = f.readlines()

    roxiedata = {}
    parse_version(roxiedata, content)
    parse_cadata_filepath(roxiedata, content)
    parse_section(roxiedata, content, 'BLOCK', ['type', 'phi', 'current', 'alpha'])
    parse_section(roxiedata, content, 'PLOT2D', ['zxaxis'])
    parse_section(roxiedata, content, 'EULER', ['no','x','y', 'alph', 'bet'])
    parse_section(roxiedata, content, 'LAYER', ['no','symm','typexy', 'blocks'])

    with open(roxiedata['cadata']['filepath']) as f:
            cadata_content = f.readlines()


    parse_version(roxiedata['cadata'], cadata_content)
    parse_section(roxiedata['cadata'], cadata_content, 'CABLE', ['No','height','width_o'])
    parse_section(roxiedata['cadata'], cadata_content, 'CONDUCTOR', ['No','Name','Strand', 'Filament', 'Trans'])
    parse_section(roxiedata['cadata'], cadata_content, 'INSUL', ['No','Name','Radial', 'Azimut', 'Comment'])
    return roxiedata

def get_section_data_by_name(section_list, data_name):
    for data in section_list:
        if data_name == data['Name']: return data
    return None

    #def make_block(x_dim, y_dim1, y_dim2, r, phi, alpha, nco):

def float_from_dict(dictionary, name): return float(dictionary[name])
def int_from_dict(dictionary, name): return int(dictionary[name])

def get_block_geom_data_list(roxiedata):
    block_data_list = roxiedata['BLOCK']
    cable_data = roxiedata['cadata']
    euler_data = roxiedata['EULER']
    layer_data = roxiedata['LAYER']

    block_geom_data_list = []
    for i, block_data in enumerate(block_data_list):
        block_geom_data_list.append({})
        block_geom_data = block_geom_data_list[-1]
        condname = block_data['condname']
        conddata = get_section_data_by_name(cable_data['CONDUCTOR'], condname)
        cablegeomname = conddata['CableGeom.']
        cablegeomdata = get_section_data_by_name(cable_data['CABLE'], cablegeomname)

        insulname = conddata['Insul']
        insuldata = get_section_data_by_name(cable_data['INSUL'], insulname)

        #print "Conductor name: ", condname
        #print "---------------------------"
        #print "block data:", block_data
        #print "conddata:", conddata
        #print "cablegeomdata:", cablegeomdata
        block_geom_data['height'] = float_from_dict(cablegeomdata,'height')
        block_geom_data['width_i'] = float_from_dict(cablegeomdata,'width_i')
        block_geom_data['width_o'] = float_from_dict(cablegeomdata,'width_o')
        block_geom_data['radius'] = float_from_dict(block_data,'radius')
        block_geom_data['phi'] = float_from_dict(block_data,'phi')
        block_geom_data['alpha'] = float_from_dict(block_data,'alpha')
        block_geom_data['nco'] = int_from_dict(block_data,'nco')
        block_geom_data['insul_radial'] = float_from_dict(insuldata,'Radial')
        block_geom_data['insul_azimut'] = float_from_dict(insuldata,'Azimut')
    return block_geom_data_list

def test_parse_roxiefile():
    roxiedata = parse_roxiefile('/home/eetakala/git/readroxie/', 'TEST.data')
    print roxiedata['BLOCK']
    print roxiedata['PLOT2D']
    print roxiedata['cadata']

def test_parse_roxiefile2():
    roxiedata = parse_roxiefile('/home/eetakala/git/readroxie/','TEST.data')
    print roxiedata['BLOCK'][0]

if __name__ == '__main__':
    test_parse_roxiefile()
    #test_parse_roxiefile2()



