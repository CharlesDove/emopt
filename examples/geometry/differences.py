"""Demonstration of how shapes in EMopt can be combined using the difference boolean
operation.

To run this script:

    $ python3 differences.py
"""
import emopt
import matplotlib.pyplot as plt

c1 = emopt.geometry.Circle(0, 0, 2.0, mat_val=2.0)
c2 = emopt.geometry.Circle(1.0, 0, 1.5, mat_val=2.0)
diff = c1.subtract(c2)

# Subtracting these two circles should produce only 1 polygon
print(f'Number of polygons in difference = {len(diff)}')

# Show the result
plt.plot(c1.xs, c1.ys, 'b.-')
plt.plot(c2.xs, c2.ys, 'c.-')
plt.plot(diff[0].xs, diff[0].ys, 'r.--')
plt.axis('equal')
plt.show()

# Generate a grid and display it
X = 5
Y = 5
dx = dy = 0.05
grid = emopt.grid.StructuredMaterial2D(X, Y, dx, dy)

# Need to move the polygon since the grid origin is in the bottom left
diff[0].translate(X/2, Y/2)

grid.add_primitives(diff)
domain = emopt.misc.DomainCoordinates(0,X,0,Y,0,0,dx,dy,1)

plt.imshow(grid.get_values_in(domain).real, extent=[0,X,0,Y])
plt.show()
