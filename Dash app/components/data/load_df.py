#from zlib import DEF_BUF_SIZE
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd

def cartera(DATA_PATH, filename):
    cierre_cart = pd.read_csv(DATA_PATH.joinpath(filename), low_memory=False,
                            dtype={'edad':'float',
                                  'cedula':'category'})
    cierre_cart['fec nacimiento'] = cierre_cart['fec nacimiento'].astype('datetime64[ns]')
    cierre_cart['fec solicitud'] = cierre_cart['fec solicitud'].astype('datetime64[ns]')
    cierre_cart['fec aproba'] = cierre_cart['fec aproba'].astype('datetime64[ns]')
    cierre_cart['fec desembolso'] = cierre_cart['fec desembolso'].astype('datetime64[ns]')
    cierre_cart['fec ult.pago'] = cierre_cart['fec ult.pago'].astype('datetime64[ns]')
    cierre_cart['fec proximo pago'] = cierre_cart['fec proximo pago'].astype('datetime64[ns]')
    cierre_cart['vencimiento final'] = cierre_cart['vencimiento final'].astype('datetime64[ns]')
    cierre_cart['reg date'] = cierre_cart['reg date'].astype('datetime64[ns]')
    drop_columns = ['nro solicitud', 'pagare', 'sucursal', 'fec solicitud', 'sucursal.1',
                'region.1', 'municipio', 'sucursales']
    cierre_cart.drop(labels=drop_columns, axis=1, inplace=True)
    cierre_cart = cierre_cart[~cierre_cart['saldo obligacion'].isin([45270281317, 44799785497])]
    cierre_cart['dia_pago'] = cierre_cart['fec ult.pago'].dt.day
    cierre_cart['dia_semana'] = cierre_cart['fec ult.pago'].dt.day_name()
    cierre_cart['año_pago'] = cierre_cart['fec ult.pago'].dt.year
    cierre_cart['mes_pago'] = cierre_cart['fec ult.pago'].dt.month
    cierre_cart['reg año'] = cierre_cart['reg date'].dt.year
    cierre_cart['reg mes'] = cierre_cart['reg date'].dt.month
    cierre_cart = cierre_cart[cierre_cart['dias vencido']<41]

    # Merge with colocacion to fill some null values
    df2 = colocacion(DATA_PATH, 'colocacion.xlsx')
    estrato = df2[['obligacion', 'estrato']]
    profesion = df2[['obligacion', 'profesion']]

    cierre_cart = cierre_cart.merge(estrato, how='left', on='obligacion')
    cierre_cart = cierre_cart.merge(profesion, how='left', on='obligacion')

    # Adding coordinates
    coord = pd.read_csv(DATA_PATH.joinpath('municipio.csv'), low_memory=False)
    coord.rename(columns={'Municipio':'municipio cliente'}, inplace=True)

    cierre_cart = cierre_cart.merge(coord, how='left', on='municipio cliente')
    
    return cierre_cart

def colocacion(DATA_PATH, filename):
    colocacion = pd.read_excel(DATA_PATH.joinpath(filename))
    colocacion.drop(labels='Unnamed: 54', axis=1, inplace=True)
    colocacion.columns = colocacion.columns.str.lower().str.strip()
    df_obj = colocacion.select_dtypes(['object'])
    colocacion[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    colocacion[df_obj.columns] = df_obj.apply(lambda x: x.str.lower())
    colocacion['mes_desembolso'] = colocacion['fec_desembolso'].dt.to_period('M').dt.to_timestamp()
    colocacion['año_desembolso'] = colocacion['fec_desembolso'].dt.to_period('Y').dt.to_timestamp()
    colocacion['año_desembolso'] = colocacion['año_desembolso'].dt.year
    colocacion['nombre_mes'] = colocacion['mes_desembolso'].dt.month

    return colocacion

def modelo(DATA_PATH, filename):
    df_modelo = pd.read_csv(DATA_PATH.joinpath(filename), sep=',', encoding='ISO-8859-1')
    modelo_vars=['responsable de hogar', 'tipo de vivienda', 'sector',
             'nivel de estudios', 'actividad economica', 'mujer cabeza de familia',
             'estado civil', 'genero', 'regional', 'monto',
             'tasa n.a.m.v', 'cuotas pactadas', 'edad', 'classification']

    df_modelo = df_modelo[df_modelo.columns[df_modelo.columns.isin(modelo_vars)]]

    # Correct values greater than 100
    df_modelo.loc[df_modelo['tasa n.a.m.v'] > 100, 'tasa n.a.m.v'] = df_modelo['tasa n.a.m.v']/100

    df_modelo.dropna(axis = 0, how = 'any', inplace = True)
    df_modelo.columns = ['sector', 'regional', 'actividad_econ',
                  'vivienda', 'estado_civil', 'genero',
                  'educ', 'mujer_cabeza', 'responsable_hogar',
                  'edad', 'monto', 'cuotas',
                  'tasa', 'classification']

    categorical = ['sector', 'regional', 'actividad_econ',
                   'vivienda', 'estado_civil', 'genero',
                   'educ', 'mujer_cabeza', 'responsable_hogar']

    ## Standard Scaler 
    scaler = StandardScaler()
    scaler = scaler.fit(df_modelo[['edad', 'monto', 'cuotas', 'tasa']])

    ## One hot encoder 

    encoder = OneHotEncoder(drop='first')
    encoder = encoder.fit(df_modelo[categorical])

    return scaler, encoder, df_modelo

def segmentacion(DATA_PATH, filename):
    df_segmentacion = pd.read_csv(DATA_PATH.joinpath(filename), low_memory=False,
                                  dtype={'edad':'float', 'estrato':'category',
                                  'cedula':'category'})
    df_segmentacion['fecha de nacimiento'] = df_segmentacion['fecha de nacimiento'].astype('datetime64[ns]')
    df_segmentacion['fec ult.pago'] = df_segmentacion['fec ult.pago'].astype('datetime64[ns]')
    df_segmentacion['fec proximo pago'] = df_segmentacion['fec proximo pago'].astype('datetime64[ns]')
    df_segmentacion['vencimiento final'] = df_segmentacion['vencimiento final'].astype('datetime64[ns]')

    return df_segmentacion




    

