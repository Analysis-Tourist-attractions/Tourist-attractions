from __init__ import df, X, y
import final_model_lgbm import LGBM
import matplotlib.pyplot as plt
from matplotlib import rc 

pred = LGBM(X,y,5,42)

#실제 y값
y_value = y.values.reshape(1,-1)
residual = y_value - pred
df['residual'] = residual.reshape(-1,1)

# ylim 설정을 위한 min, max
min = df.residual.min()
max = df.residual.max()

# 글꼴체 설정
rc('font', family = 'Malgun Gothic') 

# 전체 도시 그래프 잔차 개별 확인

def get_residual_plot(df):   
    
    unique_li= df.unstack().index.unique()
    for i in unique_li:
        tmp = df.loc[i, 'residual']
        plt.figure(figsize=(12, 8))
        tmp.plot(kind='line', x='date',y='residual', marker = 'P', color = 'black')
        plt.title(i)
        plt.xlabel('date')
        plt.ylabel('residual')
        plt.ylim([min,max])
        plt.show()

# 전체 도시 잔차 그래프 확인
def total_residual_plot_area():
    
    df = df.reset_index()
    top_place = df['local'].unique()
    fig, axs = plt.subplots(nrows=63, ncols=4, figsize=(100, 600))

    for i, place in enumerate(top_place):
        row = i // 4
        col = i % 4
        df_place = df[df['local'] == place]
        x = df_place['date']
        y = df_place['residual']

        axs[row][col].plot(x, y, marker='P', color='black')
        axs[row][col].set_title(place, fontsize=50)
        axs[row][col].set_xlabel('date', fontsize=12)
        axs[row][col].set_ylabel('residual', fontsize=12)
        axs[row][col].set_ylim([min,max]) # y축 limit 설정
        axs[row][col].axhline(0, color='red', linestyle='solid') # y = 0 추가
        axs[row][col].fill_between(x, 0, y, facecolor='skyblue', alpha=.8,) # 밀도 색칠

    plt.subplots_adjust(wspace=0.3, hspace=0.4)
    plt.show()