"""
Materials dictionary

Copyright 2025  Matthew Newville, The University of Chicago, newville@cars.uchicago.edu
using the MIT license
"""
import os
from collections import namedtuple
import platformdirs

from .chemparser import chemparse
from .xray import mu_elam, atomic_mass

MATERIALS = None

Material = namedtuple('Material', ('formula', 'density', 'name', 'categories'))

def get_user_materialsfile(create_folder=False):
    """return file name for user-specific materials.dat file

    Args:
        create_folder (bool): whether to ensure the configuration folder exists [False]

    Notes:
      The location will depend on operating system, being

        Linux:   $HOME/.config/xraydb/materials.dat
        MacOS:   $HOME//Library/Application Support/xraydb/materials.dat
        Windows: $HOME/AppData/Local/xraydb/xraydb/materials.dat

      (or replacing 'Local' with 'Roaming' if using a Roaming Profile) where
      $HOME is the home folder of the user, found as os.path.expanduser('~').
    """
    conf_dir = platformdirs.user_config_dir('xraydb')
    if create_folder and not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
    return os.path.join(conf_dir, 'materials.dat')

def _read_materials_db():
    """
    return MATERIALS dictionary, creating it if needed
    """
    global MATERIALS
    if MATERIALS is None:
        # initialize materials table
        MATERIALS = {}

        def read_materialsfile(fname):
            with open(fname, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()
            for line in lines:
                line = line.strip()
                if len(line) > 2 and not line.startswith('#'):
                    words = [i.strip() for i in line.split('|')]
                    formula = None
                    if len(words) == 4: # valid material line
                        name = words[0].lower()
                        density = float(words[1])
                        categories = [w.strip() for w in words[2].split(',')]
                        formula = words[3].replace(' ', '')
                        MATERIALS[name] = Material(formula, density, name, categories)

        # first, read from standard list
        local_dir, _ = os.path.split(__file__)
        fname = os.path.join(local_dir, 'materials.dat')
        if os.path.exists(fname):
            read_materialsfile(fname)
        # next, read from users materials file
        fname = get_user_materialsfile()
        if os.path.exists(fname):
            read_materialsfile(fname)

    return MATERIALS

def material_mu(name, energy, density=None, kind='total'):
    """X-ray attenuation length (in 1/cm) for a material by name or formula

    Args:
        name (str): chemical formul or name of material from materials list.
        energy (float or ndarray):   energy or array of energies in eV
        density (None or float):  material density (gr/cm^3).
        kind (str): 'photo' or 'total' for whether to return the
                    photo-absorption or total cross-section ['total']
    Returns:
        absorption length in 1/cm

    Notes:
        1.  material names are not case sensitive,
            chemical compounds are case sensitive.
        2.  mu_elam() is used for mu calculation.
        3.  if density is None and material is known, that density will be used.

    Examples:
        >>> material_mu('H2O', 10000.0)
        5.32986401658495
    """
    global MATERIALS
    if MATERIALS is None:
        MATERIALS = _read_materials_db()
    formula = None
    _density  = None
    mater = MATERIALS.get(name.lower(), None)
    if mater is None:
        for val in MATERIALS.values():
            if name.lower() == val[0].lower(): # match formula
                mater = val
                break

    # default to using passed in name as a formula
    if formula is None:
        if mater is None:
            formula = name
        else:
            formula = mater.formula
    if density is None and mater is not None:
        density = mater.density
    if density is None:
        raise Warning('material_mu(): must give density for unknown materials')

    mass_tot, mu = 0.0, 0.0
    for elem, frac in chemparse(formula).items():
        mass  = frac * atomic_mass(elem)
        mu   += mass * mu_elam(elem, energy, kind=kind)
        mass_tot += mass
    return density*mu/mass_tot


def material_mu_components(name, energy, density=None, kind='total'):
    """material_mu_components: absorption coefficient (in 1/cm) for a compound

    Args:
        name (str): chemical formul or name of material from materials list.
        energy (float or ndarray):   energy or array of energies in eV
        density (None or float):  material density (gr/cm^3).
        kind (str):  'photo' or 'total'for whether to
                  return photo-absorption or total cross-section ['total']

    Returns:
        dict for constructing mu per element,
        with elements 'mass' (total mass), 'density', and
       'elements' (list of atomic symbols for elements in material).
        For each element, there will be an item (atomic symbol as key)
        with tuple of (stoichiometric fraction, atomic mass, mu)

    Examples:
        >>> xraydb.material_mu('quartz', 10000)
        50.36774553547068
        >>> xraydb.material_mu_components('quartz', 10000)
        {'mass': 60.0843, 'density': 2.65, 'elements': ['Si', 'O'],
        'Si': (1, 28.0855, 33.87943243018506), 'O': (2.0, 15.9994, 5.952824815297084)}
     """
    global MATERIALS
    if MATERIALS is None:
        MATERIALS = _read_materials_db()
    mater = MATERIALS.get(name.lower(), None)
    if mater is None:
        formula = name
        if density is None:
            raise Warning('material_mu(): must give density for unknown materials')
    else:
        formula = mater.formula
        density = mater.density

    out = {'mass': 0.0, 'density': density, 'elements':[]}
    for atom, frac in chemparse(formula).items():
        mass  = atomic_mass(atom)
        mu    = mu_elam(atom, energy, kind=kind)
        out['mass'] += frac*mass
        out[atom] = (frac, mass, mu)
        out['elements'].append(atom)
    return out


def get_material(name):
    """look up material name, return formula and density


    Args:
        name (str): name of material or chemical formula

    Returns:
        chemical formula, density of material

    Examples:
        >>> xraydb.get_material('kapton')
        ('C22H10N2O5', 1.43)

    See Also:
       find_material()

    """
    material = find_material(name)
    if material is None:
        return None
    return material.formula, material.density

def find_material(name):
    """look up material name, return material instance

    Args:
        name (str): name of material or chemical formula

    Returns:
        material instance

    Examples:
        >>> xraydb.find_material('kapton')
        Material(formula='C22H10N2O5', density=1.42, name='kapton', categories=['polymer'])

    See Also:
       get_material()

    """
    global MATERIALS
    if MATERIALS is None:
        MATERIALS = _read_materials_db()

    mat =  MATERIALS.get(name.lower(), None)

    if mat is not None:
        return mat
    for mat in MATERIALS.values():
        if mat.formula == name:
            return mat
    return None



def get_materials(force_read=False, categories=None):
    """get dictionary of all available materials

    Args:
        force_read (bool): whether to force a re-reading of the
                         materials database [False]
        categories (list of strings or None): restrict results
                         to those that match category names

    Returns:
        dict with keys of material name and values of Materials instances

    Examples:
        >>> for name, m in xraydb.get_materials().items():
        ...      print(name, m)
        ...
        water H2O 1.0
        lead Pb 11.34
        aluminum Al 2.7
        kapton C22H10N2O5 1.42
        polyimide C22H10N2O5 1.42
        nitrogen N 0.00125
        argon Ar 0.001784
        ...

    """
    global MATERIALS

    if force_read or MATERIALS is None:
        MATERIALS = _read_materials_db()
    if categories is not None:
        if not isinstance(categories, list):
            categories = list([categories])
        filtered_materials = {
            k: v for k,v in MATERIALS.items() if
            (set(v.categories) & set(categories))
        }
        return filtered_materials
    return MATERIALS


def add_material(name, formula, density, categories=None):
    """add a material to the users local material database

    Args:
        name (str): name of material
        formula (str): chemical formula
        density (float): density
        categories (list of strings or None): list of category names

    Returns:
        None

    Notes:
        the data will be saved to the file 'xraydb/materials.dat' in the users
        configuration folder, and will be useful in subsequent sessions.


    Examples:
        >>> xraydb.add_material('becopper', 'Cu0.98e0.02', 8.3, categories=['metal'])

    """
    global MATERIALS
    if MATERIALS is None:
        MATERIALS = _read_materials_db()
    formula = formula.replace(' ', '')

    if categories is None:
        categories = []
    MATERIALS[name.lower()] = Material(formula, float(density), name, categories)

    text = ['# user-specific database of materials',
            '# name  |  density |  categories | formula']


    fname = get_user_materialsfile(create_folder=True)
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as fh:
            text = [s[:-1] for s in fh.readlines()]

    # catstring = ', '.join(categories)
    text.append(f" {name:s} | {density:.6g} | {', '.join(categories):s} | {formula:s}")
    text.append('')
    with open(fname, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(text))
