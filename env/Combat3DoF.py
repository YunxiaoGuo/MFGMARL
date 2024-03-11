# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:45:39 2024

@author: whoops
"""
from random import random
import numpy as np
import copy
import pickle

class Combat3DoF:
    def __init__(self, n):
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
        self.player = ['main','opponent']
        self.delta_t = 1

        
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
        self.v = [[3*[0] for j in range(self.n)] for i,item in enumerate(self.player)]
        
        state = [self.x,self.y,self.z,self.v]
        info = [self.x,self.y,self.z,self.v]
        done = False
        reward = [[0]*self.n for i,item in enumerate(self.player)]
        return state,reward,done,info
        
    def step(self,act_r,act_b):
        """simulation one step after set actions

        Returns
        -------
        done: bool
            whether the game is done
        act_r = [[[a_x_r_1,a_y_r_1,a_z_r_1],[a_x_r_2,a_y_r_2,a_z_r_2]...,]]
        3xn
        """
        act = [act_r,act_b]
        self.r = [self.x,self.y,self.z]
        for i,item in enumerate(self.player):
            for j in range(self.n):
                for k,item in enumerate(self.r):
                    self.v[i][j][k] += self.delta_t*act[i][j][k]
                    self.r[k][i][j] += self.delta_t*(self.v[i][j][k]+self.delta_t*0.5)
        self.x = self.r[0]
        self.y = self.r[1]
        self.z = self.r[2]
        state = [self.x,self.y,self.z,self.v]
        reward = self.get_reward()
        info = [self.x,self.y,self.z,self.v]
        done = self.check_done()
        return state,reward,done,info
        
    def check_done(self):
        return False
    
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
    
    def get_reward(self):
        return 0        
        
        
    def test_data_generator(self):
        state,reward,done,info = self.reset()
        info_ = copy.deepcopy(info)
        data = [info_]
        for t in range(199):
            act = [[[random(),random(),random()] for j in range(self.n)] for i,item in enumerate(self.player)]
            state,reward,done,info = self.step(act[0], act[1])
            info_ = copy.deepcopy(info)
            data.append(info_)
        data = np.array(data)
        np.save("./test_data.npy",data)
        return data

#if '__main__' == __name__:
#    env = Combat3DoF(5)
#    data = env.test_data_generator()
        
        
        