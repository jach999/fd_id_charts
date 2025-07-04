# Here are all the helpers functions

# Set the bars width and the font based on the number of data points
def SetBarsWithAndSize(data_points):
    if data_points < 90:
        figwidth = 18
        fontsize = 12
    elif data_points > 130:
        figwidth = 26
        fontsize = 9
    else:
        figwidth = data_points/5
        fontsize = (1080/data_points)

    return figwidth, fontsize