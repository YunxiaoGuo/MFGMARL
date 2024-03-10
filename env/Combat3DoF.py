# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:45:39 2024

@author: whoops
"""
from random import random

class env:
    def __init__(self, n, **kwargs):
        """
        Parameters
        ----------
        config: str or Config Object
            if config is a string, then it is a name of builtin config,
                builtin config are stored in python/magent/builtin/config
                kwargs are the arguments to the config
            if config is a Config Object, then parameters are stored in that object
        """
        self.n = n
        self.x_area_r = [100,150]
        self.y_area_r = [100,150]
        self.x_area_b = [200,250]
        self.y_area_b = [200,250]
        self.z_area = [500,550]
        
    def random_generator(self,area):
        x = [random()*area[0]+area[1]-area[0] for i in range(self.n)]
        return x
        
    def reset(self):
        """reset environment
        x = [[x_r_1,x_r_2,...],[x_b_1,x_b_2,...]]
        y = [[y_r_1,y_r_2,...],[y_b_1,y_b_2,...]]
        ...
        """
        self.x = [self.random_generator(self.x_area_r),self.random_generator(self.x_area_b)]
        self.y = [self.random_generator(self.y_area_r),self.random_generator(self.y_area_b)]
        self.z = [self.random_generator(self.z_area),self.random_generator(self.z_area)]
        
        
        
    def step(self,act):
        """simulation one step after set actions

        Returns
        -------
        done: bool
            whether the game is done
        act_r = [[[a_x_r_1,a_y_r_1,a_z_r_1],[a_x_r_2,a_y_r_2,a_z_r_2]...,]]
        3xn
        """
        
        
        
        
        
        
        
        
        
        