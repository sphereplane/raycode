#include<iostream>
#include<random>
#include<cmath>
#include<ctime>
#include<omp.h>

/* 
Compilation command: g++ sp_raycode.cpp
Compilation command (OMP parallelism):  g++ -fopenmp sp_raycode.cpp
*/

int main()
{
    // Set initial number of points and rays per point
    int Npts = 1e3;
    int Nrays = 1e3;

    // Counters for the number of successful rays and plane-crossing rays
    int Nsuccess = 0;
    int Ncross = 0;
    
    // Set up RNG
    std::default_random_engine generator (time(NULL));
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    // Pick points randomly on the sphere
    # pragma omp parallel for
    for (int j=0; j<Npts; j++)
    {
        // Calculate the coordinates of the point
        double thp = acos( 2.0*dist(generator) - 1.0 );
        double phip = 2*M_PI*dist(generator);

        double x = sin(thp)*cos(phip);
        double y = sin(thp)*sin(phip);
        double z = cos(thp);

        // Randomly generate a ray from the point uniformly on a sphere.
        # pragma omp parallel for reduction (+ : Nsuccess,Ncross)
        for (int i=0; i<Nrays; i++)
        //while (Nsuccess < Nrays)
        {
            // Randomly generate a ray uniformly along the sphere.
            
            // Uniform sampling in th
            double thr = acos( 2.0*dist(generator) - 1.0 );
            double phir = 2*M_PI*dist(generator);

            // Calculate the ray endpoint in Cartesian coordinates
            double xr = sin(thr)*cos(phir);
            double yr = sin(thr)*sin(phir);
            double zr = cos(thr);

            // Calculate the dot product of the point position vector and the ray vector.
            // If the dot product is negative, the ray is below the point's local horizon and should be skipped.
            if (x*xr + y*yr + z*zr < 0)
                continue;
            else
            {
                Nsuccess++;
                // Record the ray as crossing the xy-plane if its z-component is negative (z > 0) / positive (z < 0).
                if (copysign(1.0,z)*zr < 0)
                    Ncross++;
            }
        }

    }

    // Calculate the fraction of plane-crossing rays
    double frac = double(Ncross) / double( std::max(1, Nsuccess) );


    // Print the results to the console.
    printf("==================== SPHEREPLANE NUMERICAL SIMULATION ====================\n\n");
    printf("Total rays attempted: %29d\n", Npts*Nrays);
    printf("Number of successful rays: %24d\n", Nsuccess);
    printf("Number of crossing rays: %26d\n", Ncross);
    printf("Fraction of crossing rays: %24.8f\n", double(Ncross)/double(Nsuccess));
    printf("Estimate of Pi: 1/f = %29.8f\n", double(Nsuccess)/double(Ncross));

    return 0;
}
