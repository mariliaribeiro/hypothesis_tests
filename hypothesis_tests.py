from scipy.stats import chi2_contingency, chi2
import pandas as pd

class ChiSquareTest:
  def __init__(self, observed_values, prob=0.95):
    self.observed_values = observed_values
    chi2_statistic, p_value, ddof, expected_values = chi2_contingency(self.observed_values)
    self.expected_values = pd.DataFrame(data=expected_values, index=self.observed_values.index, columns=self.observed_values.columns)
    self.ddof = ddof
    self.prob = prob
    self.alpha = 1.0 - self.prob
    self.p_value = p_value
    self.chi2_statistic = chi2_statistic
    self.critical_value = chi2.ppf(q=self.prob, df=self.ddof)  
    self.acept_H0_by_chi2_statistic = None
    self.acept_H0_by_p_value = None
    self.label_chi2_statistic = None
    self.label_p_value = None

  def chi_square_test(self):
    if self.critical_value > self.chi2_statistic:
      self.acept_H0_by_chi2_statistic = True
      self.label_chi2_statistic = '>'
    else:
      self.acept_H0_by_chi2_statistic = False
      self.label_acept_H0_by_chi2_statistic = '<='
      
    if self.p_value <= self.alpha:
      self.acept_H0_by_p_value = False
      self.label_p_value = '<='
    else:
      self.acept_H0_by_p_value = True
      self.label_p_value = '>'

    return self
