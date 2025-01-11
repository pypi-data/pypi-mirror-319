# Testing the package for small size
from TaxSEA_in_python import get_IDs
from TaxSEA_in_python.TaxSEA import TaxSEA

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum'] # Input must be a list.

# Converting bacterial names into NCBI ID
bacterial_ID = get_IDs.NCBI(bacteria) 
# print(bacterial_ID)

# Finding the Taxons correspond to those bacterial names.
bacterial_taxon = get_IDs.Taxon(bacteria)
# print(bacterial_taxon)



TaxSEA_test_data = {"Faecalibacterium_prausnitzii" : -4.040, "Bacteroides_uniformis" : -3.859, "Roseburia_hominis" : -4.260,  
                    "Alistipes_putredinis" : -9.212, "Bacteroides_dorei" : -5.111, "Eubacterium_rectale" : -2.893, 
                    "Fusicatenibacter_saccharivorans" : -6.185, "Ruminococcus_gnavus" : 3.924, "Dorea_longicatena" : -4.671, 
                    "Agathobaculum_butyriciproducens" : -4.489, "Blautia_obeum" :  -3.367, "Anaerostipes_hadrus" : -4.240, 
                    "Ruminococcus_bicirculans" : -1.715, "Blautia_wexlerae" : -1.446, "Eubacterium_eligens" :  -2.751, 
                    "Akkermansia_muciniphila" : -2.422,  "Bacteroides_ovatus" : -3.888, "Bacteroides_faecis" :  -3.734,
                    "Dorea_formicigenerans" :  -3.753, "Roseburia_inulinivorans" : -3.438 }


results_df = TaxSEA(TaxSEA_test_data)