""" MA3.py

Student: Leo Hassler
Mail: leo.hassler.5867@student.uu.se
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
from functools import reduce
from numba import njit
import concurrent.futures as futures

# Exc1
def approximate_pi(n):
    # n is the number of points

    # Write your code here
    n_c = 0
    x_circle = []
    y_circle = []
    x_square = []
    y_square = []

    for i in range(n):
         x_cord = random.uniform(-1,1)
         y_cord = random.uniform(-1,1)
         dist = x_cord**2 + y_cord**2
         
         if dist <= 1:
              n_c += 1
              x_circle.append(x_cord)
              y_circle.append(y_cord)
         else: 
              x_square.append(x_cord)
              y_square.append(y_cord)
         
    pi = (4*n_c)/n
    print(f"Number of points: {n}")
    print(f"Approximation of pi: {pi}")
    plt.figure()
    plt.scatter(x_circle, y_circle, color='red')
    plt.scatter(x_square, y_square, color='blue')
    plt.axis("equal")
    plt.savefig(f"Approx_pi_n_{n}.png")
    plt.close()
    
    return pi

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points

    # d is the number of dimensions of the sphere 
    n_c = 0
    for i in range(n):
        point = [random.uniform(-1,1) for z in range(d)]
        squares = map(lambda val: val**2, point)
        r = reduce(lambda a, b: a+b, squares)
        if r<=1:
             n_c += 1
    V_d = 2**d*(n_c/n)
               
    return V_d

#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points

    # d is the number of dimensions of the sphere
    V_d_exact = m.pi**(d/2)/m.gamma((d/2)+1)
    
    return V_d_exact

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points

    # d is the number of dimensions of the sphere
    #np is the number of processes
    n_c = 0
    for i in range(n):
        point = [random.uniform(-1,1) for z in range(d)]
        squares = map(lambda val: val**2, point)
        r = reduce(lambda a, b: a+b, squares)
        if r<=1:
             n_c += 1
    V_d = 2**d*(n_c/n)
               
    return V_d
    

#Exc4: Help code for parallell computing
def points_in_sphere(n, d):
        n_c = 0
        for i in range(n):
            point = [random.uniform(-1,1) for z in range(d)]
            squares = map(lambda val: val**2, point)
            r = reduce(lambda a, b: a+b, squares)
            if r<=1:
                n_c += 1
        return n_c

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallell(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    points_per_process = n//np
    futures = []
    
    with future.ProcessPoolExecutor(max_workers = np) as excecutor:
        for i in range(np):
            points_this_process = points_per_process
            if i == 0:
                points_this_process += n%np
            f = excecutor.submit(points_in_sphere, points_this_process, d)
            futures.append(f)
    
    total_nc = 0
    for f in futures:
         total_nc += f.result()

    V_d = 2**d*(total_nc/n)
    return V_d

        
    
         
         
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    approx_2 = sphere_volume(n, d)
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(n,d)}")
    print(f"Approximate volume of {d} dimensional sphere = {approx_2}")

    n = 100000
    d = 11
    approx_11 = sphere_volume(n, d)
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(n,d)}")
    print(f"Approximate volume of {d} dimensional sphere = {approx_11}")

    # Exc3
    for i in range(3):
        n = 1000000
        d = 11
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    
    for i in range(3):
        n = 1000000
        d = 11
        start = pc()
        sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3: Numba time of {d} and {n}: {stop-start}")
    
    
   

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    approx = sphere_volume(n, d) 
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print(approx)
    start = pc()
    approx_2 = sphere_volume_parallell(n, d)
    stop = pc()
    print(f"Exc4: Parallel time of {d} and {n}: {stop-start}")
    print(approx_2)

    
    

if __name__ == '__main__':
	main()
     

