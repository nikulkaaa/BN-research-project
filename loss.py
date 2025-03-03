import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



'''
This is just the text output copied from the Colab. You can plot your own
iterations here is you so wish to visualize the plateauing of the loss. 
'''


data = """iteration: 500 loss: 0.0364 lr: 0.005
iteration: 1000 loss: 0.0201 lr: 0.005
iteration: 1500 loss: 0.0190 lr: 0.005
iteration: 2000 loss: 0.0177 lr: 0.005
iteration: 2500 loss: 0.0172 lr: 0.005
iteration: 3000 loss: 0.0163 lr: 0.005
iteration: 3500 loss: 0.0157 lr: 0.005
iteration: 4000 loss: 0.0153 lr: 0.005
iteration: 4500 loss: 0.0155 lr: 0.005
iteration: 5000 loss: 0.0146 lr: 0.005
iteration: 5500 loss: 0.0140 lr: 0.005
iteration: 6000 loss: 0.0139 lr: 0.005
iteration: 6500 loss: 0.0131 lr: 0.005
iteration: 7000 loss: 0.0132 lr: 0.005
iteration: 7500 loss: 0.0131 lr: 0.005
iteration: 8000 loss: 0.0135 lr: 0.005
iteration: 8500 loss: 0.0127 lr: 0.005
iteration: 9000 loss: 0.0124 lr: 0.005
iteration: 9500 loss: 0.0128 lr: 0.005
iteration: 10000 loss: 0.0122 lr: 0.005
iteration: 10500 loss: 0.0132 lr: 0.02
iteration: 11000 loss: 0.0128 lr: 0.02
iteration: 11500 loss: 0.0121 lr: 0.02
iteration: 12000 loss: 0.0118 lr: 0.02
iteration: 12500 loss: 0.0116 lr: 0.02
iteration: 13000 loss: 0.0109 lr: 0.02
iteration: 13500 loss: 0.0105 lr: 0.02
iteration: 14000 loss: 0.0108 lr: 0.02
iteration: 14500 loss: 0.0103 lr: 0.02
iteration: 15000 loss: 0.0102 lr: 0.02
iteration: 15500 loss: 0.0103 lr: 0.02
iteration: 16000 loss: 0.0095 lr: 0.02
iteration: 16500 loss: 0.0097 lr: 0.02
iteration: 17000 loss: 0.0093 lr: 0.02
iteration: 17500 loss: 0.0092 lr: 0.02
iteration: 18000 loss: 0.0093 lr: 0.02
iteration: 18500 loss: 0.0089 lr: 0.02
iteration: 19000 loss: 0.0089 lr: 0.02
iteration: 19500 loss: 0.0086 lr: 0.02
iteration: 20000 loss: 0.0085 lr: 0.02
iteration: 20500 loss: 0.0085 lr: 0.02
iteration: 21000 loss: 0.0083 lr: 0.02
iteration: 21500 loss: 0.0083 lr: 0.02
iteration: 22000 loss: 0.0082 lr: 0.02
iteration: 22500 loss: 0.0082 lr: 0.02
iteration: 23000 loss: 0.0078 lr: 0.02
iteration: 23500 loss: 0.0079 lr: 0.02
iteration: 24000 loss: 0.0078 lr: 0.02
iteration: 24500 loss: 0.0078 lr: 0.02
iteration: 25000 loss: 0.0075 lr: 0.02
iteration: 25500 loss: 0.0077 lr: 0.02
iteration: 26000 loss: 0.0075 lr: 0.02
iteration: 26500 loss: 0.0076 lr: 0.02
iteration: 27000 loss: 0.0076 lr: 0.02
iteration: 27500 loss: 0.0073 lr: 0.02
iteration: 28000 loss: 0.0073 lr: 0.02
iteration: 28500 loss: 0.0073 lr: 0.02
iteration: 29000 loss: 0.0072 lr: 0.02
iteration: 29500 loss: 0.0069 lr: 0.02
iteration: 30000 loss: 0.0071 lr: 0.02
iteration: 30500 loss: 0.0071 lr: 0.02
iteration: 31000 loss: 0.0069 lr: 0.02
iteration: 31500 loss: 0.0070 lr: 0.02
iteration: 32000 loss: 0.0066 lr: 0.02
iteration: 32500 loss: 0.0069 lr: 0.02
iteration: 33000 loss: 0.0067 lr: 0.02
iteration: 33500 loss: 0.0066 lr: 0.02
iteration: 34000 loss: 0.0069 lr: 0.02
iteration: 34500 loss: 0.0065 lr: 0.02
iteration: 35000 loss: 0.0066 lr: 0.02
iteration: 35500 loss: 0.0067 lr: 0.02
iteration: 36000 loss: 0.0064 lr: 0.02
iteration: 36500 loss: 0.0065 lr: 0.02
iteration: 37000 loss: 0.0067 lr: 0.02
iteration: 37500 loss: 0.0063 lr: 0.02
iteration: 38000 loss: 0.0066 lr: 0.02
iteration: 38500 loss: 0.0064 lr: 0.02
iteration: 39000 loss: 0.0064 lr: 0.02
iteration: 39500 loss: 0.0062 lr: 0.02
iteration: 40000 loss: 0.0062 lr: 0.02
iteration: 40500 loss: 0.0063 lr: 0.02
iteration: 41000 loss: 0.0062 lr: 0.02
iteration: 41500 loss: 0.0060 lr: 0.02
iteration: 42000 loss: 0.0060 lr: 0.02
iteration: 42500 loss: 0.0059 lr: 0.02
iteration: 43000 loss: 0.0060 lr: 0.02
iteration: 43500 loss: 0.0060 lr: 0.02
iteration: 44000 loss: 0.0060 lr: 0.02
iteration: 44500 loss: 0.0059 lr: 0.02
iteration: 45000 loss: 0.0062 lr: 0.02
iteration: 45500 loss: 0.0060 lr: 0.02
iteration: 46000 loss: 0.0058 lr: 0.02
iteration: 46500 loss: 0.0057 lr: 0.02
iteration: 47000 loss: 0.0058 lr: 0.02
iteration: 47500 loss: 0.0057 lr: 0.02
iteration: 48000 loss: 0.0056 lr: 0.02
iteration: 48500 loss: 0.0058 lr: 0.02
iteration: 49000 loss: 0.0058 lr: 0.02
iteration: 49500 loss: 0.0057 lr: 0.02
iteration: 50000 loss: 0.0055 lr: 0.02
iteration: 50500 loss: 0.0056 lr: 0.02
iteration: 51000 loss: 0.0055 lr: 0.02
iteration: 51500 loss: 0.0054 lr: 0.02
iteration: 52000 loss: 0.0054 lr: 0.02
iteration: 52500 loss: 0.0055 lr: 0.02
iteration: 53000 loss: 0.0054 lr: 0.02
iteration: 53500 loss: 0.0055 lr: 0.02
iteration: 54000 loss: 0.0056 lr: 0.02
iteration: 54500 loss: 0.0055 lr: 0.02
iteration: 55000 loss: 0.0055 lr: 0.02
iteration: 55500 loss: 0.0055 lr: 0.02
iteration: 56000 loss: 0.0053 lr: 0.02
iteration: 56500 loss: 0.0052 lr: 0.02
iteration: 57000 loss: 0.0052 lr: 0.02
iteration: 57500 loss: 0.0053 lr: 0.02
iteration: 58000 loss: 0.0051 lr: 0.02
iteration: 58500 loss: 0.0052 lr: 0.02
iteration: 59000 loss: 0.0053 lr: 0.02
iteration: 59500 loss: 0.0053 lr: 0.02
iteration: 60000 loss: 0.0054 lr: 0.02
iteration: 60500 loss: 0.0052 lr: 0.02
iteration: 61000 loss: 0.0052 lr: 0.02
iteration: 61500 loss: 0.0052 lr: 0.02
iteration: 62000 loss: 0.0050 lr: 0.02
iteration: 62500 loss: 0.0053 lr: 0.02
iteration: 63000 loss: 0.0051 lr: 0.02
iteration: 63500 loss: 0.0052 lr: 0.02
iteration: 64000 loss: 0.0052 lr: 0.02
iteration: 64500 loss: 0.0049 lr: 0.02
iteration: 65000 loss: 0.0051 lr: 0.02
iteration: 65500 loss: 0.0050 lr: 0.02
iteration: 66000 loss: 0.0051 lr: 0.02
iteration: 66500 loss: 0.0049 lr: 0.02
iteration: 67000 loss: 0.0049 lr: 0.02
iteration: 67500 loss: 0.0049 lr: 0.02
iteration: 68000 loss: 0.0050 lr: 0.02
iteration: 68500 loss: 0.0048 lr: 0.02
iteration: 69000 loss: 0.0047 lr: 0.02
iteration: 69500 loss: 0.0049 lr: 0.02
iteration: 70000 loss: 0.0049 lr: 0.02
iteration: 70500 loss: 0.0049 lr: 0.02
iteration: 71000 loss: 0.0048 lr: 0.02
iteration: 71500 loss: 0.0048 lr: 0.02
iteration: 72000 loss: 0.0048 lr: 0.02
iteration: 72500 loss: 0.0048 lr: 0.02
iteration: 73000 loss: 0.0044 lr: 0.02
iteration: 73500 loss: 0.0047 lr: 0.02
iteration: 74000 loss: 0.0047 lr: 0.02
iteration: 74500 loss: 0.0048 lr: 0.02
iteration: 75000 loss: 0.0047 lr: 0.02
iteration: 75500 loss: 0.0047 lr: 0.02
iteration: 76000 loss: 0.0046 lr: 0.02
iteration: 76500 loss: 0.0047 lr: 0.02
iteration: 77000 loss: 0.0047 lr: 0.02
iteration: 77500 loss: 0.0048 lr: 0.02
iteration: 78000 loss: 0.0047 lr: 0.02
iteration: 78500 loss: 0.0046 lr: 0.02
iteration: 79000 loss: 0.0046 lr: 0.02
iteration: 79500 loss: 0.0047 lr: 0.02
iteration: 80000 loss: 0.0045 lr: 0.02
iteration: 80500 loss: 0.0047 lr: 0.02
iteration: 81000 loss: 0.0045 lr: 0.02
iteration: 81500 loss: 0.0047 lr: 0.02
iteration: 82000 loss: 0.0046 lr: 0.02
iteration: 82500 loss: 0.0044 lr: 0.02
iteration: 83000 loss: 0.0045 lr: 0.02
iteration: 83500 loss: 0.0046 lr: 0.02
iteration: 84000 loss: 0.0046 lr: 0.02
iteration: 84500 loss: 0.0044 lr: 0.02
iteration: 85000 loss: 0.0045 lr: 0.02
iteration: 85500 loss: 0.0044 lr: 0.02
iteration: 86000 loss: 0.0045 lr: 0.02
iteration: 86500 loss: 0.0045 lr: 0.02
iteration: 87000 loss: 0.0043 lr: 0.02
iteration: 87500 loss: 0.0044 lr: 0.02
iteration: 88000 loss: 0.0044 lr: 0.02
iteration: 88500 loss: 0.0044 lr: 0.02
iteration: 89000 loss: 0.0044 lr: 0.02
iteration: 89500 loss: 0.0043 lr: 0.02
iteration: 90000 loss: 0.0043 lr: 0.02
iteration: 90500 loss: 0.0042 lr: 0.02
iteration: 91000 loss: 0.0045 lr: 0.02
iteration: 91500 loss: 0.0042 lr: 0.02
iteration: 92000 loss: 0.0043 lr: 0.02
iteration: 92500 loss: 0.0045 lr: 0.02
iteration: 93000 loss: 0.0044 lr: 0.02
iteration: 93500 loss: 0.0043 lr: 0.02
iteration: 94000 loss: 0.0044 lr: 0.02
iteration: 94500 loss: 0.0043 lr: 0.02
iteration: 95000 loss: 0.0042 lr: 0.02
iteration: 95500 loss: 0.0044 lr: 0.02
iteration: 96000 loss: 0.0043 lr: 0.02
iteration: 96500 loss: 0.0042 lr: 0.02
iteration: 97000 loss: 0.0045 lr: 0.02
iteration: 97500 loss: 0.0042 lr: 0.02
iteration: 98000 loss: 0.0040 lr: 0.02
iteration: 98500 loss: 0.0043 lr: 0.02
iteration: 99000 loss: 0.0041 lr: 0.02
iteration: 99500 loss: 0.0040 lr: 0.02
iteration: 100000 loss: 0.0045 lr: 0.02
iteration: 100500 loss: 0.0041 lr: 0.02
iteration: 101000 loss: 0.0043 lr: 0.02
iteration: 101500 loss: 0.0044 lr: 0.02
iteration: 102000 loss: 0.0042 lr: 0.02
iteration: 102500 loss: 0.0041 lr: 0.02
iteration: 103000 loss: 0.0044 lr: 0.02
iteration: 103500 loss: 0.0043 lr: 0.02
iteration: 104000 loss: 0.0042 lr: 0.02
iteration: 104500 loss: 0.0041 lr: 0.02
iteration: 105000 loss: 0.0042 lr: 0.02
iteration: 105500 loss: 0.0040 lr: 0.02
iteration: 106000 loss: 0.0041 lr: 0.02
iteration: 106500 loss: 0.0041 lr: 0.02
iteration: 107000 loss: 0.0041 lr: 0.02
iteration: 107500 loss: 0.0042 lr: 0.02
iteration: 108000 loss: 0.0040 lr: 0.02
iteration: 108500 loss: 0.0042 lr: 0.02
iteration: 109000 loss: 0.0040 lr: 0.02
iteration: 109500 loss: 0.0041 lr: 0.02
iteration: 110000 loss: 0.0041 lr: 0.02
iteration: 110500 loss: 0.0038 lr: 0.02
iteration: 111000 loss: 0.0040 lr: 0.02
iteration: 111500 loss: 0.0039 lr: 0.02
iteration: 112000 loss: 0.0041 lr: 0.02
iteration: 112500 loss: 0.0041 lr: 0.02
iteration: 113000 loss: 0.0040 lr: 0.02
iteration: 113500 loss: 0.0038 lr: 0.02
iteration: 114000 loss: 0.0039 lr: 0.02
iteration: 114500 loss: 0.0041 lr: 0.02
iteration: 154500 loss: 0.0034 lr: 0.005
iteration: 155000 loss: 0.0033 lr: 0.005
iteration: 155500 loss: 0.0034 lr: 0.005
iteration: 156000 loss: 0.0031 lr: 0.005
iteration: 156500 loss: 0.0032 lr: 0.005
iteration: 157000 loss: 0.0032 lr: 0.005
iteration: 157500 loss: 0.0032 lr: 0.005
iteration: 158000 loss: 0.0032 lr: 0.005
iteration: 158500 loss: 0.0033 lr: 0.005
iteration: 159000 loss: 0.0032 lr: 0.005
iteration: 159500 loss: 0.0032 lr: 0.005
iteration: 160000 loss: 0.0032 lr: 0.005
iteration: 160500 loss: 0.0032 lr: 0.005
iteration: 161000 loss: 0.0032 lr: 0.005
iteration: 161500 loss: 0.0031 lr: 0.005
iteration: 162000 loss: 0.0034 lr: 0.005
iteration: 162500 loss: 0.0033 lr: 0.005
iteration: 163000 loss: 0.0031 lr: 0.005
iteration: 163500 loss: 0.0031 lr: 0.005
iteration: 164000 loss: 0.0032 lr: 0.005
iteration: 164500 loss: 0.0035 lr: 0.02
iteration: 165000 loss: 0.0036 lr: 0.02
iteration: 165500 loss: 0.0035 lr: 0.02
iteration: 166000 loss: 0.0035 lr: 0.02
iteration: 166500 loss: 0.0035 lr: 0.02
iteration: 167000 loss: 0.0036 lr: 0.02
iteration: 167500 loss: 0.0035 lr: 0.02
iteration: 168000 loss: 0.0035 lr: 0.02
iteration: 168500 loss: 0.0036 lr: 0.02
iteration: 169000 loss: 0.0036 lr: 0.02
iteration: 169500 loss: 0.0035 lr: 0.02
iteration: 170000 loss: 0.0035 lr: 0.02
iteration: 170500 loss: 0.0036 lr: 0.02
iteration: 171000 loss: 0.0036 lr: 0.02
iteration: 171500 loss: 0.0035 lr: 0.02
iteration: 172000 loss: 0.0036 lr: 0.02
iteration: 172500 loss: 0.0035 lr: 0.02
iteration: 173000 loss: 0.0036 lr: 0.02
iteration: 173500 loss: 0.0034 lr: 0.02
iteration: 174000 loss: 0.0035 lr: 0.02
iteration: 174500 loss: 0.0035 lr: 0.02
iteration: 175000 loss: 0.0035 lr: 0.02
iteration: 175500 loss: 0.0035 lr: 0.02
iteration: 176000 loss: 0.0034 lr: 0.02
iteration: 176500 loss: 0.0036 lr: 0.02
iteration: 177000 loss: 0.0035 lr: 0.02
iteration: 177500 loss: 0.0035 lr: 0.02
iteration: 178000 loss: 0.0033 lr: 0.02
iteration: 178500 loss: 0.0034 lr: 0.02
iteration: 179000 loss: 0.0034 lr: 0.02
iteration: 179500 loss: 0.0035 lr: 0.02
iteration: 180000 loss: 0.0034 lr: 0.02
iteration: 180500 loss: 0.0035 lr: 0.02
iteration: 181000 loss: 0.0036 lr: 0.02
iteration: 181500 loss: 0.0035 lr: 0.02
iteration: 182000 loss: 0.0035 lr: 0.02
iteration: 182500 loss: 0.0036 lr: 0.02
iteration: 183000 loss: 0.0035 lr: 0.02
iteration: 183500 loss: 0.0032 lr: 0.02
iteration: 184000 loss: 0.0034 lr: 0.02
iteration: 184500 loss: 0.0035 lr: 0.02
iteration: 185000 loss: 0.0034 lr: 0.02
iteration: 185500 loss: 0.0034 lr: 0.02
iteration: 186000 loss: 0.0033 lr: 0.02
iteration: 186500 loss: 0.0033 lr: 0.02
iteration: 187000 loss: 0.0035 lr: 0.02
iteration: 187500 loss: 0.0034 lr: 0.02
iteration: 188000 loss: 0.0035 lr: 0.02
iteration: 188500 loss: 0.0035 lr: 0.02
iteration: 189000 loss: 0.0034 lr: 0.02
iteration: 189500 loss: 0.0035 lr: 0.02
iteration: 190000 loss: 0.0033 lr: 0.02
iteration: 190500 loss: 0.0035 lr: 0.02
iteration: 191000 loss: 0.0034 lr: 0.02
iteration: 191500 loss: 0.0034 lr: 0.02
iteration: 192000 loss: 0.0035 lr: 0.02
iteration: 192500 loss: 0.0035 lr: 0.02
iteration: 193000 loss: 0.0034 lr: 0.02
iteration: 193500 loss: 0.0033 lr: 0.02
iteration: 194000 loss: 0.0034 lr: 0.02
iteration: 194500 loss: 0.0035 lr: 0.02
iteration: 195000 loss: 0.0033 lr: 0.02
iteration: 195500 loss: 0.0035 lr: 0.02
iteration: 196000 loss: 0.0034 lr: 0.02
iteration: 196500 loss: 0.0033 lr: 0.02
iteration: 197000 loss: 0.0034 lr: 0.02
iteration: 197500 loss: 0.0034 lr: 0.02
iteration: 198000 loss: 0.0033 lr: 0.02
iteration: 198500 loss: 0.0033 lr: 0.02
iteration: 199000 loss: 0.0033 lr: 0.02
iteration: 199500 loss: 0.0034 lr: 0.02
iteration: 200000 loss: 0.0034 lr: 0.02
iteration: 200500 loss: 0.0034 lr: 0.02
iteration: 201000 loss: 0.0032 lr: 0.02
iteration: 201500 loss: 0.0034 lr: 0.02
iteration: 202000 loss: 0.0033 lr: 0.02
iteration: 202500 loss: 0.0034 lr: 0.02
iteration: 203000 loss: 0.0033 lr: 0.02
iteration: 203500 loss: 0.0033 lr: 0.02
iteration: 204000 loss: 0.0033 lr: 0.02
iteration: 204500 loss: 0.0033 lr: 0.02
iteration: 205000 loss: 0.0033 lr: 0.02"""

# create lists for the losses and iterations. 
# for loop is to extract the data from the string-text
iterations, losses = [], []
for line in data.split("\n"):
    parts = line.split()
    iter_num = int(parts[1])
    loss = float(parts[3])
    iterations.append(iter_num)
    losses.append(loss)

# Compute moving average (window=5)
window_size = 5
smoothed_losses = np.convolve(losses, np.ones(window_size)/window_size, mode='valid')

# Compute regression factor over last 20000 iterrations
num_points = 20000
X_last = np.array(iterations[-num_points:]).reshape(-1, 1)
y_last = np.array(losses[-num_points:])

# fit model to give the coefficient over the last 20000
reg = LinearRegression().fit(X_last, y_last)
slope = reg.coef_[0]*20000

# Print regression slope
print(f"Regression Slope over last {num_points} points: {slope:.6f}")
if slope < 0:
    print("Loss is trending DOWNWARDS (good).")
elif slope > 0:
    print("Loss is trending UPWARDS (bad).")
else:
    print("Loss is stable (no significant trend).")

# Plot
plt.figure(figsize=(10, 5))
plt.plot(iterations, losses, label="Raw Loss", color='blue', alpha=0.6)
plt.plot(iterations[window_size-1:], smoothed_losses, label="Smoothed Loss (Moving Avg)", color='red', linestyle='dashed')
plt.xlabel("Iteration")
plt.ylabel("Loss")
plt.title("Loss Curve with Moving Average")
plt.legend()
plt.grid()
plt.show()