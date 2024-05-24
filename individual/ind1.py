#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from multiprocessing import Process, Manager

E = 1e-7  # Точность

def series1(x, eps, results):
    s = 0
    n = 0
    while True:
        term = (-1)**n * x**(2*n) / math.factorial(2*n)
        if abs(term) < eps:
            break
        s += term
        n += 1
    results["series1"] = s

def series2(x, eps, results):
    s = 0
    n = 1
    while True:
        term = (-1)**(n-1) * x / n
        if abs(term) < eps:
            break
        s += term
        n += 1
    results["series2"] = s

def main():
    with Manager() as manager:
        results = manager.dict({"series1": 0, "series2": 0})

        x1 = 0.3
        control1 = math.cos(x1)

        x2 = 0.4
        control2 = math.log(x2 + 1)

        process1 = Process(target=series1, args=(x1, E, results))
        process2 = Process(target=series2, args=(x2, E, results))

        process1.start()
        process2.start()

        process1.join()
        process2.join()

        sum1 = results["series1"]
        sum2 = results["series2"]

        print(f"x1 = {x1}")
        print(f"Sum of series 1: {sum1:.7f}")
        print(f"Control value 1: {control1:.7f}")
        print(f"Match 1: {round(sum1, 7) == round(control1, 7)}")

        print(f"x2 = {x2}")
        print(f"Sum of series 2: {sum2:.7f}")
        print(f"Control value 2: {control2:.7f}")
        print(f"Match 2: {round(sum2, 7) == round(control2, 7)}")

if __name__ == "__main__":
    main()
