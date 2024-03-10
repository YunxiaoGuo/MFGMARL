# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:45:39 2024

@author: whoops
"""
from random import random
import numpy as np

class Combat3DoF:
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
        self.v = [self.n*[0] for i in range(2)]
        return self.state
        
    def step(self,act):
        """simulation one step after set actions

        Returns
        -------
        done: bool
            whether the game is done
        act_r = [[[a_x_r_1,a_y_r_1,a_z_r_1],[a_x_r_2,a_y_r_2,a_z_r_2]...,]]
        3xn
        """
        info = []
        done = False
        for i in range(self.n):
            self.v[i] += (act[i][0] - 2) * self.delta_v
            self.v[i] = np.clip(self.v[i], -self.v_max, self.v_max)
            self.omega[i] += (act[i][1] - 2) * self.delta_omega
            self.omega[i] = np.clip(self.omega[i], -self.omega_max, self.omega_max)
            self.theta[i] += self.theta_reg(self.omega[i] * self.delta_t)
            self.x[i] += self.v[i] * np.cos(self.theta[i]) * self.delta_t
            self.y[i] += self.v[i] * np.sin(self.theta[i]) * self.delta_t
            info.append([self.x[i], self.y[i], self.theta[i], self.v[i], self.omega[i]])
        self.state = self.get_state()
        reward = self.get_rwd()
        return self.state, reward, done, info
        
    def get_handles(self):
        """
        get the handles of the agents
        """
        handles = []
        for i,item in ['main','opponent']:
            handle = [[] for i in range(self.n)]
            handles.append(handle)
        return handles

    def get_num(self, handle):
        """ get the number of agents in a group"""
        return len(handle)
        
        
        
        
        
        