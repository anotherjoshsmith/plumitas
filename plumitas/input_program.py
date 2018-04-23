import os.path as op
import numpy as np
import pandas as pd
import mdtraj as md


def main():
    print_header()
    create_input_dict()


def print_header():
    print()
    print('-----------------------------------------------------------------------')
    print('''
    Hello friend! Thanks for choosing to set up your enhanced sampling project
    with plumitas. In my objective opinion, you've made an excellent choice.
    
        /|\          /|\          /|\          /|\          /|\          /|\  
       \\|//        \\|//        \\|//        \\|//        \\|//        \\|// 
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///      \\\|///
       \\|//        \\|//        \\|//        \\|//        \\|//        \\|// 
        \|/          \|/          \|/          \|/          \|/          \|/ 
         |            |            |            |            |            |   
    ''')
    print()
    print('-----------------------------------------------------------------------')
    print()


def create_input_dict():
    plumed = {
        'header': {},
        'groups': {},
        'collective_variables': {},
        'bias': {},
        'footer': {}
    }

    affirmative = ['y', 'yes', '']

    # load molecular configuration
    top_path = input('Please provide the path to your molecular'
                     'configuration file: ')
    base_dir = op.dirname(__file__)
    conf = op.join(base_dir, top_path)
    traj = md.load(conf)
    topology = traj.top

    # create topology table for advanced selections
    table, bonds = topology.to_dataframe()

    # HEADER SECTION
    print("Let's start with the PLUMED file header.")
    print()

    # Should restart be appended to the top of the file?
    plumed['header']['restart'] = False
    restart = input('Will this input file be used for a restart (y/n)? ')
    if restart.lower() in affirmative:
        plumed['header']['restart'] = True
    print()

    # define WHOLEMOLECULES entities
    plumed['header']['wholemolecules'] = []
    make_whole = input('Would you like to add an entity to '
                       'WHOLEMOLECULES (y/n)? ')
    while make_whole != 'n':
        print()
        selection = input('Please define an entity to add: ')
        atoms = topology.select(selection)
        filtered_table = table[table['serial'].isin(atoms)]
        residues = pd.unique(filtered_table['resSeq'])
        # TODO: fix this for the case of multiple residues
        if len(residues) == 1:
            plumed['header']['wholemolecules'].append(selection)
            make_whole = input('Would you like to add another entity '
                               'to WHOLEMOLECULES (y/n)? ')
            continue

        for res in residues:
            plumed['header']['wholemolecules'].append(f'resid {res}')

        make_whole = input('Would you like to add another entity to '
                           'WHOLEMOLECULES (y/n)? ')
    print()

    # GROUPS SECTION


if __name__ == '__main__':
    main()

