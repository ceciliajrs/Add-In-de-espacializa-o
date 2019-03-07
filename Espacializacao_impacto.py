import arcpy
import pythonaddins

class ButtonClass1(object):

    """Implementation for TCC_Python_addin.button (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):

        # Importa tabela Excel para ArcGIS
        arcpy.ExcelToTable_conversion(r'path\to\matriz_impacto.xls', r'path\to\save.dbf', 'nome')

        # Seleciona localizacoes = [1, 2, 3, 4] e separa impactos por area
        for i in range(1,5):

            arcpy.TableSelect_analysis('nome', r'path\to\split' + str(i) + '.dbf', '"Localizaca" = ' + str(i))
            
            # Conta numero de linhas das tabelas criadas
            count=arcpy.GetCount_management('split' + str(i))

            # Copia shapes das localizacoes
            for j in range(0,int(count[0])):
                arcpy.CopyFeatures_management(['ADA_SIRGAS','AID_SIRGAS','AII_SIRGAS','AAR_SIRGAS'][i-1], r'path\to\copy'+str(i)+'_'+str(j), '#', '0', '0', '0')

                arcpy.TableSelect_analysis('split' + str(i), r:'path\to\split'+str(i)+'_'+str(j), '"OID" = '+str(j))

                arcpy.JoinField_management('copy'+str(i)+'_'+str(j), 'Valor', 'split'+str(i)+'_'+str(j), 'LOCALIZACA', '#')

                arcpy.PolygonToRaster_conversion('copy'+str(i)+'_'+str(j), 'SIGNIFICAN', r'path\to\impacto'+str(i)+'_'+str(j)+'.tif', 'CELL_CENTER', 'NONE','0,0001')