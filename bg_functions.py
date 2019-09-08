import numpy as np
import pandas as pd

# Constants definition
MAX_ERROR = 10e-8

# **Auxiliary methods for the fixed point iteration algorithm**
# NOTE: These aren't mine, they're taken from Scipy optimization library.

def _relerr(actual, desired):
    return (actual - desired) / desired

def _del2(p0, p1, d):
    return p0 - np.square(p1 - p0) / d

def _valarray(shape, value=np.nan, typecode=None):
    """
    Return an array of all value.
    """

    out = np.ones(shape, dtype=bool) * value
    if typecode is not None:
        out = out.astype(typecode)
    if not isinstance(out, np.ndarray):
        out = np.asarray(out)
    return out

def _lazywhere(cond, arrays, f, fillvalue=None, f2=None):
    """
    np.where(cond, x, fillvalue) always evaluates x even where cond is False.
    This one only evaluates f(arr1[cond], arr2[cond], ...).
    For example,
    >>> a, b = np.array([1, 2, 3, 4]), np.array([5, 6, 7, 8])
    >>> def f(a, b):
        return a*b
    >>> _lazywhere(a > 2, (a, b), f, np.nan)
    array([ nan,  nan,  21.,  32.])
    Notice it assumes that all `arrays` are of the same shape, or can be
    broadcasted together.
    """
    if fillvalue is None:
        if f2 is None:
            raise ValueError("One of (fillvalue, f2) must be given.")
        else:
            fillvalue = np.nan
    else:
        if f2 is not None:
            raise ValueError("Only one of (fillvalue, f2) can be given.")

    arrays = np.broadcast_arrays(*arrays)
    temp = tuple(np.extract(cond, arr) for arr in arrays)
    tcode = np.mintypecode([a.dtype.char for a in arrays])
    out = _valarray(np.shape(arrays[0]), value=fillvalue, typecode=tcode)
    np.place(out, cond, f(*temp))
    if f2 is not None:
        temp = tuple(np.extract(~cond, arr) for arr in arrays)
        np.place(out, ~cond, f2(*temp))

    return out

# Own methods
def singlepoint_table(func, Xi, x0, method):
    '''
    Creates a table showing steps for the single-point rooting methods (fixed_point, newton_raphson).

    Parameters
    ----------
    func : function
        The function for which we are trying to find the fixed point.
    Xi : list
        List of solutions.
    x0 : float
        Initial value. It's only required in case only one iteration would be made.
    method : string
        Table processing will change depending on the method, so it's necessary to identify it.
    
    Dependencies
    ------------
    - import pandas as pd
    
    Returns
    -------
    table : pandas.DataFrame
        A 3-column table. 'Xi' is the solutions column, 'F(xi)' is the column
        containing the evaluation of those solutions in the function 'func',
        column 'Error' contains the absolute error between 'F(xi)' and 'Xi'.
    
    Explanation
    -----------
    In case there's a unique iteration (meaning 'Xi' would be empty), the a single
    row dataframe will be created.
    Otherwise, depending on the method:
        fixed_point: it'll first cast values in 'Xi' to float type, then it'll save in
    another list the values resulted from applying the function 'func' to all the
    'Xi' values. It will then compute the absolute error as |Xi+1 - Xi| in another
    list. Finally the three (3) lists will be zipped into a pandas.DataFrame.
        newton_rapshon: For this method the parameter 'Xi' is actually F(Xi)
    so 'Fxi' column will be simply 'Xi' casted into float. The error is the original
    function applied to the 'Fxi' column and the 'Xi' column is the absolute value
    between the 'error' and 'Fxi' columns.
      
    Examples
    --------
    >>> func = lambda x: x**2-3*x+2
    >>> solution, Xi = fixed_point(func, 0, 50)
    >>> tabs = singlepoint_table(func, Xi, x0, "fixed_point")
    >>> tabs
    **Renders a 3-column table** 
    
    '''
    if len(Xi) == 0:
        table = pd.DataFrame(columns=['Xi','F(xi)', 'Error'])
        table.loc[0] = [x0, func(x0), abs(func(x0) - x0)]
        return table
    else:
        if (method == "fixed_point"):
            Xi = [float(x) for x in Xi];
            Fxi = list(map(func, Xi));
            error = [abs(j-i) for j,i in zip(Fxi, Xi)]
            table = pd.DataFrame(Xi, columns=['Xi'])
            table['F(xi)'] = Fxi
            table['Error'] = error
            return table
        elif (method == "newton_raphson"):
            Fxi = [float(x) for x in Xi];
            error = list(map(func, Fxi));
            Xi = [abs(j-i) for j,i in zip(error, Fxi)]
            table = pd.DataFrame(Xi, columns=['Xi'])
            table['F(xi)'] = Fxi
            table['Error'] = error
            return table
        else:
            print("Nombre de método no válido, por favor revise los nombres de los métodos")
            
def doublepoint_table(func, Xi, error):
    '''
    Creates a table showing steps for the double-point rooting methods (secant, bisection, regula_falsi).

    Parameters
    ----------
    func : function
        The function for which we are trying to find the fixed point.
    Xi : list
        List of solutions.
    error : list
        A list containing the absolute error of each iteration. It's literally the third column.
    
    Dependencies
    ------------
    - import pandas as pd
    
    Returns
    -------
    table : pandas.DataFrame
        A 3-column table. 'Xi' is the solutions column, 'F(xi)' is the column
        containing the evaluation of those solutions in the function 'func',
        column 'Error' contains the absolute error between 'F(xi)' and 'Xi'.
    
    Explanation
    -----------
    In case there's a unique iteration (meaning 'Xi' would be empty), the a single
    row dataframe will be created.
    Otherwise, it'll compute F(xi) by adding the 'error' (absolute error) and the 'Xi'
    columns. Then it'll add each column to the dataframe.
    
    Examples
    --------
    >>> func = lambda x: x**2 - x -1
    >>> solution, Xi, error = secant(func, 1, 2, 10)
    >>> tabs = doublepoint_table(func, Xi, error)
    >>> tabs
    **Renders a 3-column table** 
    
    '''
    if len(Xi) == 0:
        table = pd.DataFrame(columns=['Xi','F(xi)', 'Error'])
        table.loc[0] = [x0, func(x0), abs(func(x0) - x0)]
        return table
    else:
        Fxi = [j + abs(i) for j,i in zip(Xi, error)]
        table = pd.DataFrame(Xi, columns=['Xi'])
        table['F(xi)'] = Fxi
        table['Error'] = error
        return table