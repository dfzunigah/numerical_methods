import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    
def fixed_point_plot(func, dataframe, x0, aprox):
    '''
    Plots the solution, aproximations, initial and final values of the f(x) = 0.

    Parameters
    ----------
    func : function
        Function to plot.
    dataframe : pandas.DataFrame
        From the 'singlepoint_table' method.
    x0 : (float) number
        Initial aproximation.
    aprox : (float) number
        Final aproximation.
    
    Dependencies
    ------------
    - import numpy as np
    - import pandas as pd
    - import matplotlib.pyplot as plt
    
    Returns
    -------
    None : ----
        When called, plots but doesn't return anything.
    
    Explanation
    -----------
    As a range is needed to plot, first it's evaluated where the solution is
    (negative or positive x-axis). According to this, it'll then evaluate if the
    aproximations span over one part of the x-axis of both negative and positive parts.
    A linear space will be created according to this, so that all needed elements can be
    plotted.
    A scatter plot is created with each point being tuples [Xi, F(xi)] taken from their
    respective columns in the provided dataframe. These represent the aproximations.
    A straight diagonal line representing 'y=x' is plotted. Function 'func' is plotted.
    Initial and final points are plotted. Title and legend location are set.
    
    Examples
    --------
    >>> func = lambda x: x**2 - x -1
    >>> solution, Xi = fixed_point(func, 0.5, 50)
    >>> tabs = singlepoint_table(func, Xi, 0.5, "fixed_point")
    >>> fixed_point_plot(func, tabs, x0, solution)
    **Plots the solution**
    '''
    x_min = dataframe['Xi'].min()
    x_max = dataframe['Xi'].max()
    if (aprox >= 0):
        if(x_min < 0):
            xpts = np.linspace(x_min, x_max, 500)
        else:
            xpts = np.linspace(0, x_max, 500)
    else:
        if(x_max > 0):
            xpts = np.linspace(x_min, x_max, 500)
        else:
            xpts = np.linspace(x_min, 0, 500)
        
    figs = dataframe.plot(kind='scatter', x='Xi', y='F(xi)', color='purple', label='Aproximaciones', figsize=(10,10))
    figs.plot(xpts, xpts, 'k')
    figs.plot(xpts, [func(x) for x in xpts], label='Función')
    figs.plot(x0, func(x0), 'ro', label='Punto incial')
    figs.plot(aprox, func(aprox), 'go', label='Punto final')
    figs.title.set_text('Gráfica de la función')
    figs.legend(loc="upper left")
    
def newton_raphson_plot(func, dataframe, x0, aprox):
    '''
    Plots the solution (root), aproximations, initial and final values of the f(x) = 0.

    Parameters
    ----------
    func : function
        Function to plot.
    dataframe : pandas.DataFrame
        From the 'doublepoint_table' method.
    x0 : (float) number
        Initial aproximation.
    aprox : (float) number
        Final aproximation.
    
    Dependencies
    ------------
    - import numpy as np
    - import pandas as pd
    - import matplotlib.pyplot as plt
    
    Returns
    -------
    None : ----
        When called, plots but doesn't return anything.
    
    Explanation
    -----------
    As a range is needed to plot, first it's evaluated where the solution is
    (negative or positive x-axis). According to this, it'll then evaluate if the
    aproximations span over one part of the x-axis of both negative and positive parts.
    A linear space will be created according to this, so that all needed elements can be
    plotted.
    In the 'df' dataframe (a copy of the provided dataframe) column 'F(xi)' contains now
    the values of the function 'func' applied to the each value of column 'Xi'. A scatter
    plot is created with tuples ['Xi', 'F(xi)']. These represent the aproximations.
    x-axis is plotted. Function 'func' is plotted. Initial and final points are plotted.
    Title and legend location are set.
    
    Examples
    --------
    >>> func = lambda x: x**2 - x -1
    >>> derivative_func = lambda x: 2*x - 1
    >>> solution, Xi = newton_rapshon(func, derivative_func, 0.5, 50)
    >>> tabs = singlepoint_table(func, Xi, 0.5, "newton_rapshon")
    >>> newton_rapshon_plot(func, tabs, x0, solution)
    **Plots the solution**
    '''
    x_min = dataframe['Xi'].min()
    x_max = dataframe['Xi'].max()
    if (aprox >= 0):
        if(x_min < 0):
            xpts = np.linspace(x_min, x_max, 500)
        else:
            xpts = np.linspace(0, x_max, 500)
    else:
        if(x_max > 0):
            xpts = np.linspace(x_min, x_max, 500)
        else:
            xpts = np.linspace(x_min, 0, 500)

    df = dataframe
    df['F(xi)'] = df['Xi'].apply(func)
    figs = dataframe.plot(kind='scatter', x='Xi', y='F(xi)', color='purple', label='Aproximaciones', figsize=(10,10))
    figs.axhline(y=0, color='k')
    figs.plot(xpts, [func(x) for x in xpts], label='Función')
    figs.plot(x0, func(x0), 'ro', label='Punto incial')
    figs.plot(aprox, func(aprox), 'go', label='Punto final')
    figs.title.set_text('Gráfica de la función')
    figs.legend(loc="upper left")
    
def doublepoint_plot(func, dataframe, a, b, aprox):
    '''
    Plots the solution, aproximations, initial and final values of the f(x) = 0.

    Parameters
    ----------
    func : function
        Function to plot.
    dataframe : pandas.DataFrame
        From the 'doublepoint_table' method.
    a, b: (float) number
        Lower (a) and upper (b) limits of the range.
    aprox : (float) number
        Final aproximation.
    
    Dependencies
    ------------
    - import numpy as np
    - import pandas as pd
    - import matplotlib.pyplot as plt
    
    Returns
    -------
    None : ----
        When called, plots but doesn't return anything.
    
    Explanation
    -----------
        
    
    Examples
    --------
    >>> func = lambda x: x**2 - x -1
    >>> solution, Xi, error = secant(func, 0, 2, 50)
    >>> tabs = doublepoint_table(func, Xi, error)
    >>> doublepoint_plot(func, tabs, 0, 2, solution)
    **Plots the solution**
    '''
    df = dataframe
    df['F(xi)'] = df['Xi'].apply(func)
    xpts = np.linspace(a, b, 500)
    figs = dataframe.plot(kind='scatter', x='Xi', y='F(xi)', color='purple', label='Aproximaciones', s=20, figsize=(10,10))
    figs.axhline(y=0, color='k')
    figs.plot(xpts, [func(x) for x in xpts], label='Función')
    figs.plot(aprox, func(aprox), 'go', markersize=12, label='Solución')
    figs.title.set_text('Gráfica de la función')
    figs.legend(loc="upper left")