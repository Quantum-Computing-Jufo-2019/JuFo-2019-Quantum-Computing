from __future__ import print_function  # allow it to run on python2 and python3

import numpy as np
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

# load matrix
qubomatrix = np.loadtxt('qubomatrix.txt')
print('Loaded matrix:\n', qubomatrix, '\n')

# convert into QUBO
qubo = {}
for index,value in np.ndenumerate(qubomatrix):
    if value != 0:
        qubo[index] = value
print('Converted matrix into QUBO for D-Wave:\n', qubo, '\n')

# embed and run on the D-Wave with 1000 reads
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(qubo, num_reads=5000)
print('Response from the D-Wave:\n', response, '\n')

# save results in results.txt
with open('results.txt','w') as file:
    file.write('energy\tnum_occurrences\tsample\n')
    for sample, energy, num_occurrences, cbf in response.record:
        file.write('%f\t%d\t%s\n' % (energy, num_occurrences, sample))
    print('Saved results in results.txt')
