#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:05:31 2021

@author: Reed Riggs
Adapted from: https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_5.html
"""

import random

#random.seed(10) #this would make random sampling replicable
sample_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] #sample list to sample from

r_samp = random.sample(sample_list, 10)
print(r_samp)

