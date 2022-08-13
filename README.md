# raycode
Numerical simulation of rays emanating from a sphere crossing a plane.  This is a supplement to the [SoME2](https://www.youtube.com/watch?v=hZuYICAEN9Y) submission "[A Sphere, A Plane, and the Early Solar System](http://sphereplane.space/a-sphere-and-a-plane)".

There are two different simulation codes available:  a C++ version, and a Python version which also plots the rays as a matplotlib figure.  The C++ version has OMP parallelization available, and can be compiled with the `-fopenmp` option if you have OpenMP installed.

Note:  The variables `Npts` and `Nrays`, which control the number of points and rays in the simulation, are initially set low for performance.  From personal testing, values above $10^4$ are preferred.
