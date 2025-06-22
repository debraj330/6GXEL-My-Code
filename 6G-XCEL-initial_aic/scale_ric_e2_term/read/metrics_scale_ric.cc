#include "srsenb/hdr/metrics_scale_ric.h"
#include "srsran/phy/utils/vector.h"

#include <float.h>
#include <iomanip>
#include <iostream>
#include <math.h>
#include <sstream>
#include <stdlib.h>
#include <unistd.h>

#include <stdio.h>
#include <string.h>

using namespace std;

namespace srsenb {

char const* const prefixes[2][9] = {
    {
        "",
        "m",
        "u",
        "n",
        "p",
        "f",
        "a",
        "z",
        "y",
    },
    {
        "",
        "k",
        "M",
        "G",
        "T",
        "P",
        "E",
        "Z",
        "Y",
    },
};

metrics_scale_ric::metrics_scale_ric(const uint32_t n_prb) : do_print(true), n_reports(10), enb(NULL), producer(NULL){
  prbs = n_prb;
}

void metrics_scale_ric::set_handle(enb_metrics_interface* enb_, scale_ric::Producer* producer_)
{
  enb = enb_;
  producer = producer_;
}

void metrics_scale_ric::toggle_print(bool b)
{
  do_print = b;
}

// Define iszero() here since it's not defined in some platforms
//static bool iszero(float x)
//{
//  return fabsf(x) < 2 * DBL_EPSILON;
//}

//void metrics_scale_ric::set_metrics_helper(uint32_t                          num_ue,
//                                        const mac_metrics_t&              mac,
//                                        const std::vector<phy_metrics_t>& phy,
//                                        const enb_metrics_t& metrics, 
//                                        bool                              is_nr)
//{}

void metrics_scale_ric::set_metrics_helper(uint32_t                          num_ue,
                                        const mac_metrics_t&              mac,
                                        const std::vector<phy_metrics_t>& phy,
                                        const enb_metrics_t& metrics, 
                                        bool                              is_nr)
{
    for (size_t i = 0; i < num_ue; i++) {
        if (i >= mac.ues.size() || ((i >= phy.size()) && !is_nr)) {
            break;
        }

        float dl_mcs = (is_nr) ? mac.ues[i].dl_mcs : phy[i].dl.mcs;
        int dl_br = (mac.ues[i].tx_brate > 0) ? (float)mac.ues[i].tx_brate / (mac.ues[i].nof_tti * 1e-3) : 0;
        float pusch_sinr = (is_nr) ? mac.ues[i].pusch_sinr : phy[i].ul.pusch_sinr;
        float pucch_sinr = (is_nr) ? mac.ues[i].pucch_sinr : phy[i].ul.pucch_sinr;
        float ul_mcs = (is_nr) ? mac.ues[i].ul_mcs : phy[i].ul.mcs;
        int ul_br = (mac.ues[i].rx_brate > 0) ? int((float)mac.ues[i].rx_brate / (mac.ues[i].nof_tti * 1e-3)) : 0;

        producer->add_key_value_to_msg("mac_rnti", std::to_string(mac.ues[i].rnti));
        producer->add_key_value_to_msg("mac_dl_cqi", std::to_string((not iszero(mac.ues[i].dl_cqi)) ? int(mac.ues[i].dl_cqi) : 0));        
        producer->add_key_value_to_msg("mac_dl_mcs", std::to_string((not isnan(dl_mcs)) ? int(dl_mcs) : 0));
        producer->add_key_value_to_msg("mac_dl_brate", std::to_string(dl_br));
        producer->add_key_value_to_msg("mac_dl_ok", std::to_string(mac.ues[i].tx_pkts - mac.ues[i].tx_errors));
        producer->add_key_value_to_msg("mac_dl_nok", std::to_string(mac.ues[i].tx_errors));

        producer->add_key_value_to_msg("phy_ul_pusch_sinr", std::to_string(phy[i].ul.pusch_sinr));
        producer->add_key_value_to_msg("phy_ul_pucch_sinr", std::to_string(phy[i].ul.pucch_sinr));
        producer->add_key_value_to_msg("phy_ul_mcs", std::to_string(phy[i].ul.mcs));
        producer->add_key_value_to_msg("mac_ul_brate", std::to_string(ul_br));
        producer->add_key_value_to_msg("mac_ul_ok", std::to_string(mac.ues[i].rx_pkts - mac.ues[i].rx_errors));
        producer->add_key_value_to_msg("mac_ul_nok", std::to_string(mac.ues[i].rx_errors));
        producer->add_key_value_to_msg("mac_ul_bsr", std::to_string(mac.ues[i].ul_buffer));  

        //MAC Metrics
        producer->add_key_value_to_msg("mac_pci", std::to_string(mac.ues[i].pci));  
        producer->add_key_value_to_msg("mac_nof_tti", std::to_string(mac.ues[i].nof_tti));  
        producer->add_key_value_to_msg("mac_cc_idx", std::to_string(mac.ues[i].cc_idx));  
        producer->add_key_value_to_msg("mac_dl_buffer", std::to_string(mac.ues[i].dl_buffer));  
        producer->add_key_value_to_msg("mac_dl_ri", std::to_string(mac.ues[i].dl_ri));  
        producer->add_key_value_to_msg("mac_dl_pmi", std::to_string(mac.ues[i].dl_pmi));  
        
        producer->add_key_value_to_msg("mac_phr", std::to_string(mac.ues[i].phr));  
        producer->add_key_value_to_msg("mac_dl_cqi_offset", std::to_string(mac.ues[i].dl_cqi_offset));  
        producer->add_key_value_to_msg("mac_ul_snr_offset", std::to_string(mac.ues[i].ul_snr_offset));  
        producer->add_key_value_to_msg("mac_ul_rssi", std::to_string(mac.ues[i].ul_rssi));  
        producer->add_key_value_to_msg("mac_fec_iters", std::to_string(mac.ues[i].fec_iters));  
        producer->add_key_value_to_msg("mac_dl_mcs_samples", std::to_string(mac.ues[i].dl_mcs_samples));  
        producer->add_key_value_to_msg("mac_ul_mcs", std::to_string(mac.ues[i].ul_mcs));  
        producer->add_key_value_to_msg("mac_ul_mcs_samples", std::to_string(mac.ues[i].ul_mcs_samples));

        // PHY Metrics
        producer->add_key_value_to_msg("phy_ul_n", std::to_string(phy[i].ul.n));
        producer->add_key_value_to_msg("phy_ul_pusch_rssi", std::to_string(phy[i].ul.pusch_rssi));
        producer->add_key_value_to_msg("phy_ul_pusch_tpc", std::to_string(phy[i].ul.pusch_tpc));
        producer->add_key_value_to_msg("phy_ul_pucch_rssi", std::to_string(phy[i].ul.pucch_rssi));
        producer->add_key_value_to_msg("phy_ul_pucch_ni", std::to_string(phy[i].ul.pucch_ni));
        producer->add_key_value_to_msg("phy_ul_turbo_iters", std::to_string(phy[i].ul.turbo_iters));        
        producer->add_key_value_to_msg("phy_ul_n_samples", std::to_string(phy[i].ul.n_samples));
        producer->add_key_value_to_msg("phy_ul_n_samples_pucch", std::to_string(phy[i].ul.n_samples_pucch));
        producer->add_key_value_to_msg("phy_dl_mcs", std::to_string(phy[i].dl.mcs));
        producer->add_key_value_to_msg("phy_dl_pucch_tpc", std::to_string(phy[i].dl.pucch_tpc));
        producer->add_key_value_to_msg("phy_dl_n_samples", std::to_string(phy[i].dl.n_samples));

        // RF Metrics
        producer->add_key_value_to_msg("rf_o", std::to_string(metrics.rf.rf_o));
        producer->add_key_value_to_msg("rf_u", std::to_string(metrics.rf.rf_o));
        producer->add_key_value_to_msg("rf_l", std::to_string(metrics.rf.rf_o));
        producer->add_key_value_to_msg("rf_error", std::to_string(metrics.rf.rf_error));

        // Sys Metrics
        producer->add_key_value_to_msg("sys_process_realmem_kB", std::to_string(metrics.sys.process_realmem_kB));
        producer->add_key_value_to_msg("sys_process_virtualmem_kB", std::to_string(metrics.sys.process_virtualmem_kB));
        producer->add_key_value_to_msg("sys_process_realmem", std::to_string(metrics.sys.process_realmem));
        producer->add_key_value_to_msg("sys_thread_count", std::to_string(metrics.sys.thread_count));
        producer->add_key_value_to_msg("sys_process_cpu_usage", std::to_string(metrics.sys.process_cpu_usage));
        producer->add_key_value_to_msg("sys_system_mem", std::to_string(metrics.sys.system_mem));
        producer->add_key_value_to_msg("sys_cpu_count", std::to_string(metrics.sys.cpu_count));
        producer->add_key_value_to_msg("n_UEs", std::to_string(num_ue));
        producer->add_key_value_to_msg("n_PRBs", std::to_string(prbs));

        producer->send_msg_to_topic();
    }
}

void metrics_scale_ric::set_metrics(const enb_metrics_t& metrics, const uint32_t period_usec)
{
  if (!do_print || enb == nullptr) {
    return;
  }

  if (metrics.rf.rf_error) {
    fmt::print("RF status: O={}, U={}, L={}\n", metrics.rf.rf_o, metrics.rf.rf_u, metrics.rf.rf_l);
  }

  if (metrics.stack.rrc.ues.size() == 0 &&
      metrics.nr_stack.mac.ues.size() == 0) {
      return;
  }
//   if (metrics.stack.rrc.ues.size() == 0) {
//     return;
//   }

  if (++n_reports > 10) {
    n_reports = 0;
    // fmt::print("\n");
    // fmt::print("          -----------------DL----------------|-------------------------UL-------------------------\n");
    // fmt::print("rat rnti  cqi  ri  mcs  brate   ok  nok  (%) | pusch  pucch  phr  mcs  brate   ok  nok  (%)    bsr\n");
  }

  set_metrics_helper(metrics.stack.rrc.ues.size(), metrics.stack.mac, metrics.phy, metrics, false);
  //set_metrics_helper(metrics.nr_stack.mac.ues.size(), metrics.nr_stack.mac, metrics.phy, metrics, true);
}

std::string metrics_scale_ric::float_to_string(float f, int digits, int field_width)
{
  std::ostringstream os;
  int                precision;
  if (isnan(f) or fabs(f) < 0.0001) {
    f         = 0.0;
    precision = digits - 1;
  } else {
    precision = digits - (int)(log10f(fabs(f + 0.0001)) - 2 * DBL_EPSILON);
  }
  if (precision == -1) {
    precision = 0;
  }
  os << std::setw(field_width) << std::fixed << std::setprecision(precision) << f;
  return os.str();
}

std::string metrics_scale_ric::float_to_eng_string(float f, int digits)
{
  const int degree = (f == 0.0) ? 0 : lrint(floor(log10f(fabs(f)) / 3));

  std::string factor;

  if (abs(degree) < 9) {
    if (degree < 0)
      factor = prefixes[0][abs(degree)];
    else
      factor = prefixes[1][abs(degree)];
  } else {
    return "failed";
  }

  const double scaled = f * pow(1000.0, -degree);
  if (degree != 0) {
    return float_to_string(scaled, digits, 5) + factor;
  } else {
    return " " + float_to_string(scaled, digits, 5 - factor.length()) + factor;
  }
}

} // namespace srsenb
