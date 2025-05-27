<h1>Very simple deterministic Finite State Machine (vsFSM) with two implementations</h1>hj1>

Two test environments are built on this vsFSM:

  1. An infectious disease model
  2. A robot controller

<h2>Infectious disease model with vsFSM</h2>

A grid is used where each cell represents a person. Each person has a
vsFSM that represents a simple SEIR model. This model has the following
states:

  - S(usceptible)
  - E(xposed)
  - I(nfected)
  - R(ecovered)
  - Dn: death by natural causes
  - Dd: death by the disease
  - Dc: Comortality, death by underlying diseases

This model contrasts with the appraoch presented by May and Anderson where 
the disease is modeled wy means of ODE's. Two examples of an ODE are 
added.

<h2>Robotic behavior implemented with a vsFSM</h2>

The robot has several compartments, e.g. Running fast, slow, stop for an obstacle, 
looking around, etc. The values of sensors as distance sensors and compass are used
in order to determine whether the vsFSM should transfer to another state. 
