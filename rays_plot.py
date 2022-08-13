import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import mpl_toolkits.mplot3d.art3d as art3d

# Set constants
# Number of points, rays, and counters for crossings
Npts = 100
Nrays = 100
Ncross = 0
Ntotal = 0

# Image colors
bgclr = '#7C7C7C'
sphereclr = '#FFEC60'
planeclr = 'xkcd:dark gray'

# Figure setup
fig = plt.figure(dpi=200, figsize=(10,10), facecolor=bgclr)
ax = plt.subplot(111, projection='3d', box_aspect=(1,1,1), facecolor=bgclr)
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_zlim(-1,1)
ax.axis('off')
ax.view_init(azim=0, elev=0.05)

# Draw a transparent sphere for reference
Nsph = 100
sphere_th = np.linspace(0, np.pi, Nsph)
sphere_phi = np.linspace(0, 2*np.pi, Nsph)
sph_x = np.outer(np.cos(sphere_phi), np.sin(sphere_th))
sph_y = np.outer(np.sin(sphere_phi), np.sin(sphere_th))
sph_z = np.outer(np.ones_like(sphere_phi), np.cos(sphere_th))

ax.plot_surface(sph_x, sph_y, sph_z, color=sphereclr, alpha=0.5, zorder=2)


# Add the xy-plane
plane = patches.Rectangle((-10,-10), 20, 20, color=planeclr, alpha=0.8, zorder=3)
ax.add_patch(plane)
art3d.pathpatch_2d_to_3d(plane, z=0, zdir='z')

# Pick random points on the sphere
for j in range (Npts):
    th_pt = np.arccos( 2*np.random.uniform(low=0,high=1) - 1 )
    phi_pt = np.random.uniform(low=0, high=2*np.pi)
    sinthp,costhp = np.sin(th_pt), np.cos(th_pt)
    sinphip,cosphip = np.sin(phi_pt), np.cos(phi_pt)
    
    xo = sinthp*cosphip
    yo = sinthp*sinphip
    zo = costhp
    
    # Create random rays from the point
    for i in range(Nrays):
        th = np.arccos( 2*np.random.uniform(low=0,high=1) - 1 )
        phi = np.random.uniform(low=0, high=2*np.pi)
        
        # Calculate the xyz coordinates of the new vector and 
        # calculate the dot product with the position on the sphere.
        sinth,costh = np.sin(th), np.cos(th)
        sinphi,cosphi = np.sin(phi), np.cos(phi)
        
        x = xo + sinth*cosphi
        y = yo + sinth*sinphi
        z = zo + costh
        
        dp = (x-xo)*xo + (y-yo)*yo + (z-zo)*zo
            
        # If the dot product is less than 0, the ray is "below the horizon",
        # which is unacceptable.
        if (dp > 0):
            # If the ray is descending (zo>0)/ ascending (zo<0)
            # it will cross the xy-plane.
            # Color the ray red and increment the counter for crossing rays.
            Ntotal += 1
            rayclr = 'xkcd:blue'
            rayalpha = 0.0075
            if np.sign(zo)*(z-zo) < 0:
                rayclr = 'xkcd:red'
                rayalpha=0.0075
                Ncross += 1

    
            # Plot the rays    
            ax.plot([xo,x], [yo,y], [zo,z], color=rayclr, alpha=rayalpha, zorder=4)
    
    # Plot the points
    ax.scatter(xo,yo,zo, color='k', marker='.', s=1, zorder=5)


# Print results to the console
print("Total rays attempted: {:>18}".format(Npts*Nrays))
print("Successful Rays: {:>23}".format(Ntotal))
print("Crossing Rays: {:>25}".format(Ncross))
print("Fraction of rays that cross: {:>11.8}".format(Ncross/Ntotal))

# Display the plotted results
plt.tight_layout()
plt.savefig("SpherePlaneSim.png", dpi=300, bbox_inches='tight')
plt.show()