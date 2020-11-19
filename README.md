# Bayesian-Network-Fire-Alarm
This project addresses the problem of fire detection in a museum, taking into account a simple fire propagation model and the uncertainty associated with the fire detectors spread over the building. The problem is modeled using a Bayesian network, and solved using the variable elimination algorithm for probabilistic inference.

# Objective
The objective of this project is to determine the room that is most probable to be on fire at time step T, as well as the probability value, given a set of measurements in the form (t; s; z) where t is the time step, s is the sensor, and z (True; False) is a boolean representing whether the sensor detected a fire or not. 

#Input Files
The problem is specified in a text file format where each line contains a list of space separated fields, where the first field should be one of the following characters:
* R - the set of Rooms R
* C — the set of connections, C, where the remaining fields are comma separated pairs of room names.
* S — the set of sensors, S, together with the corresponding rooms, having each field with the form s : r : TPR : FPR where r = l(s) is the room where sensor s is located, and TPR and FPR are its true positive and false positive rates
* P — the propagation probability P=[0; 1]
* M —a measurement where each one of the remaining fields have the form s : z where s is the sensor and z (True; False) is the measurement.
