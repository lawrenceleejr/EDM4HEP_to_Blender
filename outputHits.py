#!/usr/bin/env python

import uproot
import argparse
import numpy as np

# Set up argument parser
parser = argparse.ArgumentParser(description="Read the first event in a TTree and print branch vectors.")
parser.add_argument("-f", type=str, help="Path to the ROOT file")
parser.add_argument("-t", type=str, default="events", help="Name of the TTree in the ROOT file (default: 'myTree')")
args = parser.parse_args()

ievent = 2
# used event 0 for muon
# used event 2 for neutron
# 0 for photon
# 0 for BIB

trackerCollections = [
    "VertexBarrelCollection",
    "VertexEndcapCollection",
    "InnerTrackerBarrelCollection",
    "InnerTrackerEndcapCollection",
    "OuterTrackerBarrelCollection",
    "OuterTrackerEndcapCollection",
]

caloCollections = [
    "ECalBarrelCollection",
    "ECalEndcapCollection",
    "HCalBarrelCollection",
    "HCalEndcapCollection",
]

muonCollections = [
    "YokeBarrelCollection",
    "YokeEndcapCollection",
]

# Open the ROOT file and get the TTree
with uproot.open(args.f) as file:
    tree = file[args.t]

    # Get the data from the first event
    first_event = tree.arrays(entry_start=ievent, entry_stop=ievent+1, library="np")

    # Convert to vectors
    vectors = {key: value[0] for key, value in first_event.items()}


    trackerArrays = []
    for trackerCollection in trackerCollections:
        print(trackerCollection)
        trackerArrays.append(
            np.stack((
                vectors[f'{trackerCollection}.position.x'],
                vectors[f'{trackerCollection}.position.y'],
                vectors[f'{trackerCollection}.position.z'],
                vectors[f'{trackerCollection}.EDep']
                ),axis=1) 
            )
    trackerOutput = np.concatenate(trackerArrays)
    mask = trackerOutput[:, 3] >= 1e-3
    trackerOutput = trackerOutput[mask]
    print(trackerOutput)
    print(len(trackerOutput))


    caloArrays = []
    for caloCollection in caloCollections:
        print(caloCollection)
        caloArrays.append(
            np.stack((
            vectors[f'{caloCollection}.position.x'],
            vectors[f'{caloCollection}.position.y'],
            vectors[f'{caloCollection}.position.z'],
            vectors[f'{caloCollection}.energy']
            ),axis=1)
            )
    
    caloOutput = np.concatenate(caloArrays)
    mask = caloOutput[:, 3] >= 1e-3
    caloOutput = caloOutput[mask]
    print(caloOutput)
    print(len(caloOutput))

    muonArrays = []
    for muonCollection in muonCollections:
        print(muonCollection)
        muonArrays.append(
            np.stack((
            vectors[f'{muonCollection}.position.x'],
            vectors[f'{muonCollection}.position.y'],
            vectors[f'{muonCollection}.position.z'],
            vectors[f'{muonCollection}.energy']
            ),axis=1) 
            )

    muonOutput = np.concatenate(muonArrays)
    print(muonOutput)


    np.savetxt(args.f+"_trackerHits.csv", trackerOutput, delimiter=",", fmt="%s")
    np.savetxt(args.f+"_caloHits.csv", caloOutput, delimiter=",", fmt="%s")
    np.savetxt(args.f+"_muonHits.csv", muonOutput, delimiter=",", fmt="%s")
