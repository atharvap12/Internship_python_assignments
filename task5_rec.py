


def is_sorted(ds):
    return all(ds[i] < ds[i + 1] for i in range(len(ds)-1))


def all_subsets(indx, ds, ol, ml):
    if indx == len(ol):
        if (is_sorted(ds)):
            #print(str(ds) + " : " + str(len(ds)))
            ml = max(ml,len(ds))
            
        return ml

    ds.append(ol[indx])
    ml = all_subsets(indx + 1, ds, ol, ml)
    le = ds.pop()
    ml = all_subsets(indx + 1, ds, ol, ml)
    return ml

def outer_func(o_lis):
    indx = 0
    ds = []
    max_l = 0
    max_l = all_subsets(indx, ds, o_lis, max_l)
    return max_l


lis = [5, 8, 7, 7, 9]


print(outer_func(lis))


    