# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:40:35 2020

@author: baole
"""

import glassdoor_scraper as gs
import pandas as pd

path = "C:/Users/baole/Data Science Projects/Glassdoor Salary Project/chromedriver"
df = gs.get_jobs('data scientist',10,False, path,5)

