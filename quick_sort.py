# farbod_shahinfar
# 29/9/95
# Quick Sort


def quick_sort(lst,x=0):
    if len(lst) < 2:
        return lst
    pivot = (lst[0][x] + lst[-1][x])/2
    lst_left = []
    lst_right = []
    for i in lst:
        if i[x] <= pivot:
            lst_left.append(i)
        else:
            lst_right.append(i)
    if not lst_right:
        return lst_left
    
    lst_left = quick_sort(lst_left, x)
    lst_right = quick_sort(lst_right, x)
    
    return lst_left + lst_right
