#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import font_manager, rc

plt.rcParams['axes.unicode_minus'] = False

f_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
font_name = font_manager.FontProperties(fname=f_path).get_name()
rc('font', family=font_name)

import drawKorea as dK

dK.simpleDraw(dK.draw_korea_pd)

korea_pop = pd.read_csv('./pop_exam.csv', index_col=0)
dK.drawKorea('인구수합계', korea_pop, 'Blues')
