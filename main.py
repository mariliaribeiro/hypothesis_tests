import numpy as np
import pandas as pd
import streamlit as st

from hypothesis_tests import ChiSquareTest

st.title('Hypothesis Tests')

st.markdown('You can access the code at my [github](https://github.com/mariliaribeiro/hypothesis_tests).')

st.header('Chi-square test')
st.header('Inputs')
  
prob = st.number_input(
    'Insert the probabilit of test (1 - alpha)', key='prob', value=0.95, min_value=0.0, max_value=1.0)
    
label, col1, col2 = st.beta_columns(3)


label.subheader("Action label")
label1 = label.text_input(
    'Observed value label 1', key='l1', value='True')
label2 = label.text_input(
    'Observed value label 2', key='l2', value='False')


col1.subheader("Group 1")
observed_value1_gp1 = col1.number_input(
    'Insert the observed value 1', key='ov1_gp1', value=0)
observed_value2_gp1 = col1.number_input(
    'Insert the observed value 2', key='ov2_gp1', value=0)

col2.subheader("Group 2")
observed_value1_gp2 = col2.number_input(
    'Insert the observed value 1', key='ov1_gp2', value=0)
observed_value2_gp2 = col2.number_input(
    'Insert the observed value 2', key='ov2_gp2', value=0)

h0 = st.text_input(
    'Insert the H0', key='h0')
h1 = st.text_input(
    'Insert the the H1', key='h1')


df = pd.DataFrame({
    'group': ['group1', 'group1', 'group2', 'group2'],
    'observed_value': [observed_value1_gp1, observed_value2_gp1, observed_value1_gp2, observed_value2_gp2],
    'label_observed_value': [label1, label2, label1, label2]
})
df_observed_values = pd.crosstab(index=df['label_observed_value'], columns=df['group'],
                                 values=df['observed_value'], aggfunc='sum', margins=True, margins_name='Total')



if st.button('Run qui-square test'):
    df_aux = df_observed_values.copy()
    df_aux = df_aux.replace(0, np.nan).dropna()   
    is_empty = df_aux.empty    
    if is_empty:
        st.warning('Please insert at least 3 observed values!')
    else:
        try:
            chi_square_test = ChiSquareTest(df_observed_values, prob)   
            chi_square_test.chi_square_test()

            st.header('Outputs')
            out_col1, out_col2 = st.beta_columns(2)

            out_col1.subheader('Observed values')
            out_col1.dataframe(df_observed_values)
            out_col2.subheader('Expected values')
            out_col2.dataframe(chi_square_test.expected_values)

            output_text = '''
            - Degrees of freedom: `{ddof}`

            - Critical value {signal1} chi-square statistic: `{critical_value} {signal1} {chi2_statistic}`

            - P-value {signal2} alpha: `{p_value} {signal2} {alpha}`    
            '''.format(
                ddof=chi_square_test.ddof,
                signal1=chi_square_test.label_chi2_statistic,
                critical_value=round(chi_square_test.critical_value,2),    
                chi2_statistic=round(chi_square_test.chi2_statistic,2),
                signal2=chi_square_test.label_p_value,
                p_value=round(chi_square_test.p_value,2),    
                alpha=round(chi_square_test.alpha,2)
            )
            st.write(output_text)


            result_info = '''
            **Acept {hypothesis_op1} by chi-square statistic**

            > {text_op1}

            **Acept {hypothesis_op2} by p-value**

            > {text_op2}
            '''.format(
                hypothesis_op1='H0' if chi_square_test.acept_H0_by_chi2_statistic else 'H1', 
                text_op1=h0 if chi_square_test.acept_H0_by_chi2_statistic else h1,
                hypothesis_op2='H0' if chi_square_test.acept_H0_by_p_value else 'H1', 
                text_op2=h0 if chi_square_test.acept_H0_by_p_value else h1
            )
            st.info(result_info)
        except:
            st.warning('Please insert at least 3 observed values!')
