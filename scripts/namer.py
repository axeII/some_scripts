#!/usr/local/bin/python3

import optparse
import sys,os
import re,itertools
from random import randint
from os.path import *
import collections
import pdb

def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-r',dest='regex_on',help='Renaming files by reading and parsing throught regex',action='store_true')
    parser.add_option('-p',dest='dir_name',help='Rename all files by current directory',action='store_true')
    parser.add_option('-d',dest='static_dir',help='Rename input directories',action='store_true')
    parser.add_option('-f',dest='file_name',help='How should files be named, FILENAME')
    parser.add_option('-n',dest='no_exec',help='Dry print, just print all action not execute',action='store_true')
    parser.add_option('-c',dest='clean',help='Acts like  mv command, simple renaming',action='store_true')
    parser.add_option('-e',dest='end_name',help='end name ??',action='store_true')
    return parser.parse_args()

"""def filterArgs(args,options):
    field,paths = (list(),map(lambda x:realpath(x),args))
    [field.append(os.listdir(a) if isdir(a) and not options.sDir else [a]) for a in args]
    #nefunguje tu namer -d -f neco input
    if not options.dirN and not options.sDir:
        paths = [[x] if isfile(x) else [dirname(realpath(y)) if options.sDir else x for y in os.listdir(x)] for x in paths]
    else:
        paths = [[x] for x in paths]
    print paths
    return (list(itertools.chain.from_iterable(field)),list(itertools.chain.from_iterable(paths)),options)
"""

def get_data_params(data,file_,counting):
    new = {}
    if not basename(file_).startswith('.'):
        try:
            counting += 1
            key = basename(file_)
            new['name'] = dirname(file_)
            new['abspath'] = abspath(file_)
            new['realpath'] = realpath(file_)
            new['basename'] = basename(file_)
            new['dirname'] = dirname(file_)
            new['isfile'] = isfile(file_)
            new['isdir'] = isdir(file_)
            new['splited'] = split(file_)
            new['order'] = counting
            new['directory'] = basename(normpath(dirname(file_)))
            if isdir(file_):
                _, new['dirs'],new['files'] = list(os.walk(file_))[0]
                new['abs_files'] = []
                for _file in new['files']:
                    new['abs_files'].append(join(new['abspath'],_file))
        except Exception as e:
            print("Oy error while getting dir info - %s" % e)
        else:
            if isinstance(data,dict):
                #data.append(new)
                data[key] = new

    return (data,counting)

def file_naming(data_dict,options):

    def file_name(specific_path,input_param,number_param,isdir_,name_param = ""):
        """if opt_param or (input_param and isfile(input_param)):
            directory = dirname(specific_path)
        else:
            directory = specific_path"""
        directory = specific_path
        number = '{0:03d}'.format(number_param)
        if not isdir_:
            file_type = splitext(input_param)[1]
        else:
            file_type = ""
        if not name_param:
            edited_name = "%s/%s%s" % (directory,number,file_type)
        else:
            edited_name = "%s/%s_%s%s" % (directory,name_param,number_param,file_type)

        return edited_name

    def renaming(old_name,new_name,options):
        if options['no_exec'] and isinstance(options,dict):
            print("Renaming from %s to %s" % (basename(old_name),basename(new_name)))
            #print('old: %s\nnew: %s\n' % (old_name,new_name))
        else:
            old_directory = split(old_name)[0]
            new_directory = split(new_name)[0]

            if old_directory == new_directory:
                print("[OK] ")#,end='',flush=True)
            else:
                print("[Error] directories are not same - \n old: %s, new: %s" % (old_directory,new_directory))

            if (isfile(old_name) or isdir(old_name)) and (not isfile(new_name) and not isdir(new_name)):
                if True:
                    os.rename(old_name,new_name)

    if isinstance(data_dict,dict) and data_dict:

        # inserting backup options, set to 0 if need to work with original options
        main_options = options[1]
        data_dict = collections.OrderedDict(sorted(data_dict.items()))
        for dict_,data in data_dict.items():
            if not main_options['static_dir'] and data['isdir']:
                for f in data['abs_files']:
                    pass
                    # add file name?
                    # solve with back calling ?
                    # put into abs_files same huge structure
            if main_options['dir_name'] or main_options['file_name']:
                specific_name = ""
                if main_options['dir_name'] and main_options['file_name']:
                    raise IOError
                elif main_options['dir_name']:
                    #pdb.set_trace()
                    specific_name = data['directory']
                else:
                    specific_name = main_options['file_name']
                # would be better just put data in it ?
                new_name = file_name(data['name'],data['basename'],data['order'],data['isdir'],specific_name)
                # if file already exists do not renaming
                if isfile(new_name):
                    continue

            elif main_options['regex_on']:
                try:
                    regex_ind = re.findall(r'\d+\.?\d*',data['basename'])[-1]
                    if regex_ind.endswith('.'):
                        regex_ind = int(regex_ind[:-1])
                    elif '.' in regex_ind:
                        regex_ind = int(regex_ind.split('.')[0]) + 1
                    else:
                        try:
                            regex_ind = int(regex_ind)
                        except Exception as e:
                            print('Failed to regex file %s, reason: %s, program answer: %s' %
                                    (data['basename'],e,regex_ind))
                except IndexError:
                    regex_ind = 0
                #print(int(re.findall(r'\d+\.?\d*',data['basename'])[-1]))
                new_name = file_name(data['name'],data['basename'],regex_ind,data['isdir'],main_options['file_name'])
            else:
                new_name = file_name(data['name'],data['basename'],data['order'],data['isdir'])

            #final file renaming
            renaming(data['realpath'],new_name,main_options)

def parse_inputs(load_data = {},input_data = None):

    def check_switches(options):
        backup_options = {}
        backup_options = vars(options)
        backup_options['any'] = any([x[1] for x in vars(options).items()])
        backup_options['all'] = all([x[1] for x in vars(options).items()])

        if options.dir_name and options.file_name:
            sys.exit("Error wrong switch combination")

        #set params for later control
        return (options,backup_options)

    if input_data:
        counting = 0
        options,args = input_data
        for arg in args:
            load_data, counting = get_data_params(load_data,abspath(arg),counting)

        file_naming(load_data,check_switches(options))
    else:
        sys.exit('Empty input...')

if __name__ == "__main__":
    parse_inputs({},parse_arguments())
