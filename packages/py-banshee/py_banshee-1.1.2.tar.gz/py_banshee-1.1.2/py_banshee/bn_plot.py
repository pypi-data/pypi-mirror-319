# -*- coding: utf-8 -*-
"""
Py_BANSHEE
Authors: Paul Koot, Miguel Angel Mendoza-Lugo, Dominik Paprotny,
         Elisa Ragno, Oswaldo Morales-Nápoles, Daniël Worm

E-mail:  m.a.mendozalugo@tudelft.nl, paulkoot6@gmail.com & O.MoralesNapoles@tudelft.nl
"""

import networkx as nx
import graphviz as gv
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from IPython.display import Image
import os


def bn_visualize(parent_cell, R, names, data=None, fig_name=''):
    """ Visualize the structure of a defined Bayesian Network
 
     bn_visualize creates and saves a directed digraph presenting the
     structure of nodes and arcs of the Bayesian Network (BN), defined by
     parent_cell. The function also displays the conditional rank
     correlations at each arc defined by R.
 
 
    Parameters
    ----------
    parent_cell : list
        A list containing the structure of the BN, 
        the same as required in the bn_rankcorr function
    R : numpy.ndarray
        Rank Correlation Matrix
    names : list
        a list containing names of the nodes for the plot. Should
        be in the same order as they appear in matrix R and parent_cell
    data : pandas.core.frame.DataFrame
        the same data that can be used as input in bn_rankcorr. When this 
        argument is given as input, the nodes in the visualization contain 
        the marginal distribution of the data within each node.
    fig_name : string
        Name extension of the .png file with the Bayesian Network that
        is created: BN_visualize_'fig_name'.png. 
        The file is saved in the working directory. 
        
    Returns
    -------
    None.
    """

    G = nx.DiGraph()
    if isinstance(data, pd.DataFrame):
        for node in data:
            plt.figure()
            h = sns.histplot(data[node], kde=True)
            h.set_xlabel('x')
            h.set_title('{}'.format(node), fontsize=25)
            plt.xticks(rotation=45)
            plt.ylabel("Count", fontsize=18)
            plt.xlabel("x", fontsize=18)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.tight_layout()
            plt.savefig('histogram_{}.png'.format(node))
            G.add_node(node, image='histogram_{}.png'.format(node),
                       fontsize=0)
            plt.show()
    else:
        G.add_nodes_from(names, style='filled', fillcolor='red')
        plt.show()
       
    #edges and labels
    edgs=[]
    edglbs=[]
    for i in range(len(names)):
        parents = parent_cell[i]
        for j in parents:
            edgs.append((names[j], names[i]))
            edglbs.append(f'{round(R[j, i],2)}')
    #add edges and labels         
    for k in range(len(edgs)):
        G.add_edges_from([edgs[k]], label = edglbs[k])
    #dot file
    nx.drawing.nx_pydot.write_dot(G, f'BN_visualize_{fig_name}')
    # Convert dot file to png file
    gv.render('dot', 'pdf', f'BN_visualize_{fig_name}')
    deleteFile(f'BN_visualize_{fig_name}')

    return f'BN plot saved in : {os.getcwd()}\BN_visualize_{fig_name}.pdf' 


def deleteFile(filename):
    if os.path.exists(filename) and not os.path.isdir(filename) and not os.path.islink(filename):
        os.remove(filename)