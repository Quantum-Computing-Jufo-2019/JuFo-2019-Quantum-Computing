#!/usr/bin/env python3

from __future__ import print_function  # allow it to run on python2 and python3

import numpy as np
from dwave.system.samplers import DWaveSampler
from dwave.system import EmbeddingComposite, LazyFixedEmbeddingComposite

# packages needed for pegasus simulation
import neal
import dimod
import dwave_networkx as dnx
import networkx as nx
import dwave.embedding

# load matrix
qubomatrix = np.loadtxt('qubomatrix.txt')
print('Loaded matrix:\n', qubomatrix, '\n')

# convert into QUBO
qubo = {(i,i):0.0 for i in range(len(qubomatrix))}  # necessary to keep the order of the sample columns consistent
for index,value in np.ndenumerate(qubomatrix):
    if value != 0:
        qubo[index] = value
print('Converted matrix into QUBO for D-Wave:\n', qubo, '\n')

# create a pegasus graph and a simulation
graph = dnx.pegasus_graph(16)  # stands for a pegasus P6 graph, see https://www.dwavesys.com/sites/default/files/mwj_dwave_qubits2018.pdf
simulator = neal.SimulatedAnnealingSampler()  # this makes it use a classical simulated annealing sampler
composite = dimod.StructureComposite(simulator, graph.nodes, graph.edges)  # necessary to make it use the pegasus graph
sampler = LazyFixedEmbeddingComposite(composite)  # similar as before

response = sampler.sample_qubo(qubo, num_reads=10000, chain_strength=40)
print('Response:\n', response, '\n')
print('Embedding:\n', sampler.embedding, '\n')
print('Nodelist:\n', sampler.nodelist, '\n')
print('Edgelist:\n', sampler.edgelist, '\n')
print('Adjacency:\n', sampler.adjacency, '\n')

# save results in results.txt
with open('results.txt','w') as file:
    file.write('energy\tnum_occurrences\tsample\n')
    for sample, energy, num_occurrences, cbf in response.data():
        newsample = np.array([value for key,value in sorted(sample.items())])  # rearrange the samples so that the computed energy matches
        file.write('%f\t%d\t%s\n' % (energy, num_occurrences, np.array2string(newsample).replace('\n','')))
    print('Saved results in results.txt')

with open('embedding.txt','w') as file:
    file.write('logicalqubit\tphysicalqubits\n')
    for logicalqubit, physicalqubits in sampler.embedding.items():
        file.write('%d\t%s\n' % (logicalqubit, physicalqubits))
    print('Saved embedding in embedding.txt')
