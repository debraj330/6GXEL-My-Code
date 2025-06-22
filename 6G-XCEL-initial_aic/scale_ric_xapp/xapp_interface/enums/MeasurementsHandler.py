from enum import Enum


class MeasurementsHandler(str, Enum):
    ALL_MEASUREMENTS = "ANY"

    CQI = "ue_cqi"
    MAC_RNTI = "mac_rnti"
    MAC_DL_MCS = "mac_dl_mcs"
    MAC_DL_BRATE = "mac_dl_brate"
    MAC_DL_OK = "mac_dl_ok"
    MAC_DL_NOK = "mac_dl_nok"

    PHY_UL_PUSCH_SINR = "phy_ul_pusch_sinr"
    PHY_UL_PUCCH_SINR = "phy_ul_pucch_sinr"
    PHY_UL_MCS = "phy_ul_mcs"
    MAC_UL_BRATE = "mac_ul_brate"
    MAC_UL_OK = "mac_ul_ok"
    MAC_UL_NOK = "mac_ul_nok"
    MAC_UL_BSR = "mac_ul_bsr"

    #//MAC Metrics
    MAC_PCI = "mac_pci"
    MAC_NOF_TTI = "mac_nof_tti"
    MAC_CC_IDX = "mac_cc_idx"
    MAC_DL_BUFFER = "mac_dl_buffer"
    MAC_DL_RI = "mac_dl_ri"
    MAC_DL_PMI = "mac_dl_pmi"

    MAC_PHR = "mac_phr"
    MAC_DL_CQI_OFFSET = "mac_dl_cqi_offset"
    MAC_UL_SNR_OFFSET = "mac_ul_snr_offset"
    MAC_UL_RSSI = "mac_ul_rssi"
    MAC_FEC_ITERS = "mac_fec_iters"
    MAC_DL_MCS_SAMPLES = "mac_dl_mcs_samples"
    MAC_UL_MCS = "mac_ul_mcs"
    MAC_UL_MCS_SAMPLES = "mac_ul_mcs_samples"

    #// PHY Metrics
    PHY_UL_N = "phy_ul_n"
    PHY_UL_PUSCH_RSSI = "phy_ul_pusch_rssi"
    PHY_UL_PUSCH_TPC = "phy_ul_pusch_tpc"
    PHY_UL_PUCCH_RSSI = "phy_ul_pucch_rssi"
    PHY_UL_PUCCH_NI = "phy_ul_pucch_ni"
    PHY_UL_TURBO_ITERS = "phy_ul_turbo_iters"
    PHY_UL_N_SAMPLES = "phy_ul_n_samples"
    PHY_UL_N_SAMPLES_PUCCH = "phy_ul_n_samples_pucch"
    PHY_DL_MCS = "phy_dl_mcs"
    PHY_DL_PUCCH_TPC = "phy_dl_pucch_tpc"
    PHY_DL_N_SAMPLES = "phy_dl_n_samples"

    #// RF Metrics
    RF_O = "rf_o"
    RF_U = "rf_u"
    RF_L = "rf_l"
    RF_ERROR = "rf_error"
