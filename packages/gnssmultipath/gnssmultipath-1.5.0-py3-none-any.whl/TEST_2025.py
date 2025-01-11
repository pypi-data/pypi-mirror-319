
from gnssmultipath import GNSS_MultipathAnalysis, GNSSPositionEstimator, SP3PositionEstimator
import numpy as np

# # outputDir = r"C:\Users\perhe\Desktop\TestGNSS Jan25\Broadcasted"
# # # outputDir = r"C:\Users\perhe\Desktop\TestGNSS Jan25\SP3"
# # # rinObs = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\ObservationFiles\OPEC00NOR_S_20220010000_01D_30S_MO_3.04.rnx"
# # # rinNav = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\NavigationFiles\BRDC00IGS_R_20220010000_01D_MN.rnx"
# # rinObs = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\ObservationFiles\OPEC00NOR_S_20220010000_01D_30S_MO_3.04_croped.rnx"
# # # rinObs = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\ObservationFiles\OPEC00NOR_S_20220010000_01D_30S_MO_3.04_croped_without_approx.rnx"
# # rinNav = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\NavigationFiles\BRDC00IGS_R_20220010000_01D_MN.rnx"
# # sp3 = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\SP3\Testfile_20220101.eph"

# # analysisResults = GNSS_MultipathAnalysis(rinObs,
# #                                          broadcastNav1=rinNav,
# #                                         #  sp3NavFilename_1=sp3,
# #                                          outputDir=outputDir,
# #                                          include_SNR=True,
# #                                          plotEstimates=True)

# np.set_printoptions(suppress=True)


# rinObs = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\ObservationFiles\OPEC00NOR_S_20220010000_01D_30S_MO_3.04_croped.rnx"
# sp3 = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\SP3\Testfile_20220101.eph"
# rinNav = r"C:\Users\perhe\OneDrive\Documents\Python_skript\GNSS_repo\TestData\NavigationFiles\BRDC00IGS_R_20220010000_01D_MN.rnx"


# fasit = np.array([3149785.9652, 598260.8822, 5495348.4927])
# desired_time = np.array([2022, 1, 1, 1, 5, 30.0000000])
# desired_system = "E"  # GPS
# gnsspos, stats = GNSSPositionEstimator(rinObs,
#                                     sp3_file = sp3,
#                                     desired_time = desired_time,
#                                     desired_system = desired_system,
#                                     elevation_cut_off_angle = 20).estimate_position()

# gnsspos_sp3e, stats = SP3PositionEstimator(rinex_obs_file= rinObs,
#                                     sp3_data = sp3,
#                                     desired_time = desired_time,
#                                     desired_system = desired_system,
#                                     elevation_cut_off_angle = 20).estimate_position()


# # gnsspos_nav, stats_nav = GNSSPositionEstimator(rinObs,
# #                                     rinex_nav_file=rinNav,
# #                                     desired_time = desired_time,
# #                                     desired_system = desired_system,
# #                                     elevation_cut_off_angle = 10).estimate_position()

# diff_sp3 = np.round(fasit - gnsspos[:-1], 3)
# print("Diff SP3: ", diff_sp3.tolist())

# # diff_nav = np.round(fasit - gnsspos_nav[:-1], 3)
# # print("Diff nav: ", diff_nav.tolist())

# print(gnsspos)
# print(gnsspos_sp3e)



import sys
import os



project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_path,'src'))

os.chdir(os.path.join(project_path,'src'))



# rinObs_file = "../TestData/ObservationFiles/NMBUS_SAMSUNG_S20.20o"
# sp3Nav_file = "../TestData/SP3/NMBUS_2020 10 30.SP3"
# expected_res = "../tests/analysisResults_NMBUS.pkl"
# result = GNSS_MultipathAnalysis(rinObsFilename=rinObs_file, sp3NavFilename_1=sp3Nav_file,
#                                 outputDir = r"C:\Users\perhe\Desktop\TestGNSS Jan25\SP3\Ny fasit 2",
#                                 plotEstimates=False,
#                                 plot_polarplot=False,
#                                 include_SNR=True,
#                                 # save_results_as_compressed_pickle=True,
#                                 save_results_as_compressed_pickle=False,
#                                 )




rinObs_file =  "../TestData/ObservationFiles/OPEC00NOR_S_20220010000_01D_30S_MO_3.04_croped.rnx"
broadNav_file = "../TestData/NavigationFiles/BRDC00IGS_R_20220010000_01D_MN.rnx"
expected_res = "../tests/analysisResults_OPEC00NOR_S_20220010000_01D_30S_MO_3.04_croped.pkl"
result = GNSS_MultipathAnalysis(rinObsFilename=rinObs_file, broadcastNav1=broadNav_file,
                                outputDir = r"C:\Users\perhe\Desktop\TestGNSS Jan25\Broadcasted\Ny fasit",
                                plotEstimates=False,
                                plot_polarplot=False,
                                write_results_to_csv=False,
                                nav_data_rate=120,
                                save_results_as_compressed_pickle=True)