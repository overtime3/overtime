
import math



def vector_angle(x, y):
    """
        A method which returns the angle of a vector.

        Parameter(s):
        -------------
        x : Integer/Float
            x-axis value of vector.
        y : Integer/Float
            y-axis value of vector.

        Returns:
        --------
        theta : Integer/Float
            Angle of vector in radians.

        See also:
        ---------
            circle_label_angle
    """
    hypot = math.sqrt(x*x + y*y) # get the hypotenuse
    theta = math.asin(y / hypot) # get the corresponding vector angle
    # apply CAST rule
    if x < 0:
        theta = math.pi - theta
    if theta < 0:
        theta = theta + 2*math.pi
    return theta


def circle_label_angle(x, y):
    """
        A method which returns a readable angle given a label's vector position.

        Parameter(s):
        -------------
        x : Integer/Float
            x-axis value of vector.
        y : Integer/Float
            y-axis value of vector.

        Returns:
        --------
        angle : Integer/Float
            Readable angle of label in degrees.

        See also:
        ---------
            vector_angle
    """
    # get vector angle in radians and convert to degrees
    angle = math.degrees(vector_angle(x, y))
    # flip the label depending on where it lies on the circle.
    if angle > 90 and angle < 270:
        return angle - 180
    else:
        return angle


def bezier(p1, p2, p0=(0,0), nt=20):
    """
        A method which creates a Bézier curve between points p1 and p2 with control point p0.

        Parameter(s):
        -------------
        p1 : Tuple 
            point p1, given by x & y coordinates (x1, y1).
        p2 : Tuple 
            point p2, given by x & y coordinates (x2, y2).
        p0 : Tuple 
            point p0, given by x & y coordinates (x0, y0). Default is (0, 0).
        nt : Integer
            Number of intermediate points to create the curve. Default is 20.

        Returns:
        --------
        bezier : Dict
            Dictionary of x and y coordinates of the created Bézier curve.
    """
    bezier = {}
    bezier['x'] = [] # x values of bezier curve points
    bezier['y'] = [] # y values of bezier curve points
    # for each point along the curve.
    for i in range(0, nt+1):
        t = (1/nt) * i # curve point index 't'.
        bezier['x'].append(
            (p1['x']-2*p0[0]+p2['x'])*math.pow(t,2) + 2*t*(p0[0]-p1['x']) + p1['x']
        ) # append x value of curve point 't'.
        bezier['y'].append(
            (p1['y']-2*p0[0]+p2['y'])*math.pow(t,2) + 2*t*(p0[0]-p1['y']) + p1['y']
        ) # append y value of curve point 't'.
    return bezier
