import mdsthin
from traceback import print_exc
from collections.abc import Iterable
import argparse
import numpy as np
import h5py
import yaml


"""
read_mdsplus_channel(shot_numbers=31779, trees='KSTAR',
                     point_names='EP53:FOO', server='203.230.126.231:8005',
                     resample=None, verbose=False)

Mostly copied from connection_test.py by D. Eldon
"""
def read_mds(shot_numbers=31779, trees='KSTAR',
             point_names='EP53:FOO', server='203.230.126.231:8005',
             resample=None, rescale=None, out_filename=None, reread_data=False,
             config=None,
             verbose=False,):
    if config is not None:
        with open(config, 'r') as f:
            config = yaml.safe_load(f)
        if 'shot_numbers' in config:
            shot_numbers = config['shot_numbers']
        if 'trees' in config:
            trees = config['trees']
        if 'point_names' in config:
            point_names = config['point_names']
        if 'server' in config:
            server = config['server']
        if 'resample' in config:
            resample = config['resample']
        if 'rescale' in config:
            rescale = config['rescale']
        if 'out_filename' in config:
            out_filename = config['out_filename']
        if 'reread_data' in config:
            reread_data = config['reread_data']
        if 'verbose' in config:
            verbose = config['verbose']
    if isinstance(shot_numbers, int):
        shot_numbers = [shot_numbers]
    if isinstance(point_names, str):
        point_names = [point_names]
    if isinstance(point_names, Iterable):
        point_names = [add_slash(pn) for pn in point_names]
    if isinstance(trees, str):
        tree_dict = {trees: point_names}
    elif isinstance(trees, list):
        if len(trees) != len(point_names):
            raise ValueError('trees and point_names must be the same length')
        tree_dict = {tree: [] for tree in trees}
        for tree, pn in zip(trees, point_names):
            tree_dict[tree].append(pn)
    elif isinstance(trees, dict):
        tree_dict = {tree: [] for tree in trees}
        for tree in trees:
            if tree != "PTDATA":
                if isinstance(trees[tree], str):
                    tree_dict[tree] = [add_slash(trees[tree])]
                else:
                    tree_dict[tree] = [add_slash(pn) for pn in trees[tree]]
    
    rescale_dict = {}
    if isinstance(rescale, (int, float)):
        rescale_dict = {tree: rescale for tree in tree_dict}
    elif isinstance(rescale, list):
        if len(rescale) != len(trees):
            raise ValueError('trees and rescale must be the same length')
        for tree, rs in zip(trees, rescale):
            rescale_dict[tree] = rs
    elif isinstance(rescale, dict):
        rescale_dict = rescale

    try:
        conn = mdsthin.Connection(server)
    except BaseException:
        print_exc()
        return None
    data_dict = {}
    to_write = False
    if out_filename is not None:
        h5 = h5py.File(out_filename, 'a')
        to_write = True
    for sn in shot_numbers:
        data_dict[sn] = {tree: {} for tree in tree_dict}
        for tree in tree_dict:
            rescale_fac = 1
            if tree in rescale_dict:
                rescale_fac = float(rescale_dict[tree])
            if tree != "PTDATA":
                try:
                    if verbose:
                        print(f"    Opening tree {tree} at shot number {sn}...")
                    conn.openTree(tree, sn)
                except BaseException:
                    print("-------------------------------------------------")
                    print(f"Error in opening {tree} at shot number {sn}")
                    print(exc)
                    print("-------------------------------------------------")
                    pass
            for pn in tree_dict[tree]:
                if (not reread_data) and to_write:
                    if check_exists(h5, sn, tree, pn):
                        continue
                try:
                    if verbose:
                        print(f"        Reading signal {pn}")
                    if tree == "PTDATA":
                        pn = 'PTDATA("' + pn + '")'
                        print(f"        Reading signal {pn}")
                    if pn.startswith("PTDATA"):
                        signal = conn.get(add_resample(pn[:-1] + f", {sn})", resample, rescale_fac))
                    else:
                        signal = conn.get(add_resample(pn, resample, rescale_fac))
                    data = signal.data()
                    units = conn.get(units_of(pn)).data()
                    data_dict[sn][tree][pn] = {'data': data, 'units': units}
                    for ii in range(np.ndim(data)):
                        try:
                            if resample is None or ii != 0:
                                dim = conn.get(dim_of(pn, ii)).data() * rescale_fac
                            else:
                                dim = get_time_array(resample)

                            data_dict[sn][tree][pn][f'dim{ii}'] = dim
                        except BaseException as exc:
                            print("-------------------------------------------------")
                            print(f"Error in reading dim of {tree}: {pn} in shot "
                                    + f"number {sn}")
                            print(exc)
                            print("-------------------------------------------------")
                            pass
                    if to_write:
                        append_h5(h5, sn, tree, pn, data_dict)
                except BaseException as exc:
                    print("-------------------------------------------------")
                    print(f"Error in reading {tree}: {pn} in shot number {sn}")
                    print(exc)
                    print("-------------------------------------------------")
                    pass

    if to_write:
        h5.close()  
    
    return data_dict


def add_slash(s):
    if s.startswith("\\") or s.startswith("PTDATA"):
        return s
    ss = "\\" + s
    return r'' + ss.encode('unicode_escape').decode('utf-8')[1:]


def add_resample(pn, resample, rescale_fac):
    if resample is None:
        return pn
    if isinstance(resample, dict):
        resample = [resample['start'], resample['stop'], resample['increment']]
    
    resample = np.array(resample) / rescale_fac
    return f"resample({pn}, {resample[0]}, {resample[1]}, {resample[2]})"

def get_time_array(resample):
    if isinstance(resample, dict):
        resample = [resample['start'], resample['stop'], resample['increment']]
    return np.arange(resample[0], resample[1] + resample[2]*0.1, resample[2])


def dim_of(pn, ii):
    return f"dim_of({pn}, {ii})"


def units_of(pn):
    return f"units_of({pn})"


def check_exists(h5, shot_number, tree, point_name):
    sn = str(shot_number)
    if sn in h5:
        if tree in h5[sn]:
            pns = add_slash(point_name)
            if pns in h5[sn][tree]:
                if 'data' in h5[sn][tree][pns]:
                    return True

def append_h5(h5, shot_number, tree, point_name, data_dict):
    sntpn_dict = data_dict[shot_number][tree][point_name]
    sn = str(shot_number)
    pn = point_name
    if sn not in h5:
        h5.create_group(sn)
    if tree not in h5[sn]:
        h5[sn].create_group(tree)
    if pn in h5[sn][tree]:
        del h5[sn][tree][pn]
    h5[sn][tree].create_group(pn)
    for key in sntpn_dict:
        if isinstance(sntpn_dict[key], np.str_):
            h5[str(sn)][tree][pn].attrs[key] = sntpn_dict[key].__repr__()
        else:
            h5[str(sn)][tree][pn].create_dataset(key, data=sntpn_dict[key])


def get_args():
    parser = argparse.ArgumentParser(description='Read MDSplus channel')
    parser.add_argument('-n', '--shot_numbers', type=int, nargs='+', help='Shot number(s)')
    parser.add_argument('-t', '--trees', nargs='+', help='Tree name(s)')
    parser.add_argument('-p', '--point_names', nargs='+', help='Point name(s)')
    parser.add_argument('-s', '--server', default='203.230.126.231:8005',
                        help='Server address. Default is 203.230.126.231:8005')
    parser.add_argument('-r', '--resample', nargs='+', type=float, default=None,
                        help='Resample signal(s) by providing a list of start, stop, '
                             'and increment values. For negative value, enclose them '
                             'withing double quotes and add a space at the beginning.'
                             'Example: --resample " -0.1" 10.0 0.1')
    parser.add_argument('--rescale', nargs='+', type=float, default=None,
                        help='Rescale time dimension of trees to ensure that all of '
                             'are in same units. Especially important if resample is '
                             'used. Provide a rescaling factor to be multiplied by '
                             'time axis for each tree provides in trees option.'
                             'Example: --resample " -0.1" 10.0 0.1')
    parser.add_argument('-o', '--out_filename', default=None,
                        help='Output filename for saving data in file. Default is '
                             'None. in which case it does not save files.')
    parser.add_argument('--reread_data', action='store_true',
                        help='Will overwrite on existing data for corresponding data '
                             'entries in out_file. Default behavior is to skip reading'
                             'pointnames whose data is present.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print verbose messages')
    parser.add_argument('-c', '--config', default=None, type=str,
                        help='Configuration file containing shot_numbers, trees, '
                             'point_names, server, and other settings. If provided, '
                             'corresponding command line arguments are ignored.')
    args = parser.parse_args()
    return args

def read_mds_cli():
    args = get_args()
    data_dict = read_mds(shot_numbers=args.shot_numbers,
                         trees=args.trees,
                         point_names=args.point_names,
                         server=args.server,
                         resample=args.resample,
                         rescale=args.rescale,
                         out_filename=args.out_filename,
                         reread_data=args.reread_data,
                         verbose=args.verbose,
                         config=args.config,)

if __name__ == '__main__':
    read_mds_cli()
