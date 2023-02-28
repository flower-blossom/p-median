import matplotlib.pyplot as plt
from utils.data import readDistanceMatrix
from utils.readFile import readTSPLib
import pandas as pd 
import plotly.express as px
import numpy as np
import plotly
from utils.solution import findRadiusPoint

# solutionList = [[0, 3, 7, 15, 23, 25, 33, 39, 53, 59, 69, 95, 104, 110, 115], [1, 2, 8, 10, 20, 22, 26, 50, 52, 79, 81, 92, 102, 114, 118], [16, 19, 42, 43, 49, 64, 68, 74, 97, 106, 117], [4, 36, 38, 56, 62, 66, 72, 82], [12], [6, 37, 40, 55, 71, 73], [11, 63, 76, 87, 94, 96, 108], [13, 14, 27, 28, 29, 31, 44, 58, 60, 75, 77, 80, 85, 86, 91, 93, 119], [5, 9, 34, 35, 46, 47, 54, 61, 70, 83, 88, 89, 98, 100, 101, 103, 105, 109, 111, 113], [17, 18, 21, 24, 30, 32, 41, 45, 48, 51, 57, 65, 67, 78, 84, 90, 99, 107, 112, 116]]
# distanceMatrix = readDistanceMatrix("gr120", "distanceMatrices")
def draw(x, y, solutionList):
    # data = readTSPLib('gr120.tsp')
    # lat = []
    # lon = []
    # for point in data:
    #     lat.append(data[point].coordinate["lat"])
    #     lon.append(data[point].coordinate["lon"])
    X = [ ]
    Y = [ ]
    for cluster in solutionList:
        X.append([x[point] for point in cluster])
        Y.append([y[point] for point in cluster])

    labels = range(1,len(X)+1)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for x,y,lab in zip(X,Y,labels):
            ax.scatter(x,y,label=lab)

    colormap = plt.cm.gist_ncar #nipy_spectral, Set1,Paired  
    colorst = [colormap(i) for i in np.linspace(0, 0.9,len(ax.collections))]       
    for t,j1 in enumerate(ax.collections):
        j1.set_color(colorst[t])

    ax.legend(fontsize='small')

    plt.show()

def drawInteractive(x, y, solutionList, distanceMatrix):
    # data = readTSPLib('gr120.tsp')
    # lat = []
    # lon = []
    # for point in data:
    #     lat.append(data[point].coordinate["lat"])
    #     lon.append(data[point].coordinate["lon"])
    # X = [ ]
    # Y = [ ]
    infoPoint = []
    for idxCluster in range(len(solutionList)):
    # for idxCluster in range(1):
        for point in solutionList[idxCluster]:
            infoPoint.append([x[point], y[point], idxCluster])
    # print(infoPoint)
    df = pd.DataFrame(infoPoint, columns =['x', 'y', "index_cluster"])
    df["index_cluster"] = df["index_cluster"].astype(str)
    
    # Loading the iris dataset

    fig = px.scatter(df, x="x", y="y",
                    color="index_cluster")
    # print(df)


    for idxCluster in range(len(solutionList)):
        print(solutionList[idxCluster])
        PairOfPoints = findRadiusPoint(solutionList[idxCluster], distanceMatrix)
        print(PairOfPoints)
        if len(PairOfPoints) == 2:
            firstPoint = PairOfPoints[0]
            secondPoint = PairOfPoints[1]
            name = "Radius cluster: " + str(idxCluster)
            fig.add_scatter(x=[x[firstPoint], x[secondPoint]],y=[y[firstPoint], y[secondPoint]], name=name)

    fig.update_traces(marker=dict(size=20))
    plotly.offline.plot(fig, filename='D:\Hoc\\thuc tap\cluster\image\\test.html')
    # fig.show()

# draw(solutionList)    



