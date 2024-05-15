from scipy.stats import norm
import numpy as np 

class PutLookback:

    def __init__(self, r, T, sigma, array_of_S , t):

        self._r = r
        self._T = T
        self._sigma = sigma 
        self._array_of_S = array_of_S
        self._t = t 
        self._M0 =self.M0_t 
        self._PutPrice = self.PutPrice
    
    @property
    def sigma(self):
        return self._sigma 

    @sigma.setter
    def sigma(self, sigma):
        self._sigma = sigma

    @property
    def T(self):
        return self._T 

    @T.setter
    def T(self, T):
        self._T = T

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    
    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        self._t= t 
        
    @property
    def M0_t(self):
        return self._array_of_S.max()
    
    @property    
    def d1(self):
        return (np.log(self._array_of_S[0]/self._M0) + (self._sigma**2/2 + self._r)*(self._T - self._t)) / self._sigma*(self._T - self._t)**0.5 
    @property
    def d2(self):
        return 1- self.d1

    @property 
    def PutPrice(self):
        return  self._M0*np.exp(-self._r*(self._T-self._t))*norm.cdf(-self.d2)+\
        self._array_of_S[0]*(1+self._sigma**2/2*self._r)* norm.cdf(self.d1)\
        -self._array_of_S[0]*np.exp(-self._r*(self._T-self._t))*self._sigma**2/2*self._r*(self._M0/self._array_of_S[0])**(2*self._r/self._sigma**2)*norm.cdf(-1/self.d2)-\
        self._array_of_S[0]
    
        
