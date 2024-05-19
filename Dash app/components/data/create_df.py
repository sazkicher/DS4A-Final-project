def create_df(df, x, y, filters=None, agg_function=None, reset_idx=True, to_frame=None):
    df1 = df.groupby(x+filters)[y]

    if agg_function=='sum':
        df1 = df1.sum()
    elif agg_function=='count':
        df1 = df1.count()
    elif agg_function=='descr':
        df1 = df1.describe()
    if reset_idx:
        if to_frame!=None:
            df1 = df1.to_frame(to_frame)
        df1 = df1.reset_index()

    return df1

def filter_df(df, x, y, filters=None, agg_function=None, reset_idx=True, to_frame=None, filter_values=[None]):
    filters = filters.copy()
    filter_values = filter_values.copy()
    if all(value is None for value in filter_values):
        df1 = create_df(df, x, y, filters=[], agg_function=agg_function, reset_idx=reset_idx, to_frame=to_frame)
        return df1
    elif all(value is not None for value in filter_values):
        if x[0] in filters:
            rem_idx = filters.index(x[0])
            filter_values.pop(rem_idx)
            filters.pop(rem_idx)
        df1 = create_df(df, x, y, filters, agg_function, reset_idx, to_frame)
    elif any(value is None for value in filter_values):
        if x[0] in filters:
            rem_idx = filters.index(x[0])
            filter_values.pop(rem_idx)
            filters.pop(rem_idx)
        valid_filters = [i for i in range(len(filters)) if filter_values[i]!=None]
        filters = [filters[i] for i in valid_filters]
        filter_values = [filter_values[i] for i in valid_filters]
        df1 = create_df(df, x, y, filters=filters, agg_function=agg_function, reset_idx=reset_idx, to_frame=to_frame)
    idx = [True]*df1.shape[0]
    for i, filter in enumerate(filters):
        idx = (df1[filter]==filter_values[i])&idx
    df1 = df1[idx]

    return df1

def filter_idx(df, filters, filter_values):
    valid_filters = [i for i in range(len(filters)) if filter_values[i]!=None]
    filters = [filters[i] for i in valid_filters]
    filter_values = [filter_values[i] for i in valid_filters]
    idx = [True]*df.shape[0]
    for i, filter in enumerate(filters):
        idx = (df[filter]==filter_values[i])&idx
    return idx