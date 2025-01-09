import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy import stats
from scipy.optimize import minimize, fminbound, least_squares

import warnings
warnings.filterwarnings('ignore')

class Gld:
    """
    Generalized Lambda Distribution in CSW Parametrization Class
    
    Generalized Lambda Distribution (GLD) is a flexible family of continuous 
    probability distributions that can assume distributions with a large range of shapes. 
    Chalabi et al [2012] introduced a new parameterization of GLD, referred to as CSW 
    Parameterization, wherein the location and scale parameters are directly expressed as 
    the median and interquartile range of the distribution. The two remaining parameters 
    characterizing the asymmetry and steepness of the distribution are distinguished clearly
    in contrast to other parametrizations where they are simultaneously described by a 
    combination of tail indices. While the first two parameters of location and scale are 
    obtained from data, various methods are suggested to obtain the shape parameters. 
    
    This tool implements the CSW parameterization types of GLD, introduced by 
    Chalabi, Y., Scott, D.J., & Wuertz, D. 2012.  It provides methods for calculating parameters 
    of theoretical GLD based on empirical data, generating random sample, estimate 
    Quantile based risk measures such as VaR, ES and so on.

    GLD in CSW parameterization is a transformation of GLD in FKML form (introduced by 
    Freimer, Mudholkar, Kollia and Lin, 1988). Location and scale are directly estimated 
    from sample estimators using quantile statistics. This formulation allows for relaxed
    constraints upon support regions and for existence of moments. Its shape parameters 
    have finite domains of variation sharing the same intuitiveness as the FMKL parametrization.  
    
    Params in CSW Paramterization:
        1. Location-> median (𝜇̃)
        2. Scale -> Inter-quartile range (𝜎̃)
        3. Shape, asymmetry -> chi (𝛘) where 𝛘 ∈ (-1,1)
        4. Shape, steepness -> xi (ξ) where ξ ∈ (0,1)
        
    It is characterized by quantile function Q(u) and density quantile function f(u). 
    
    Q(u|𝜇̃,𝜎̃,𝛘,ξ) = 𝜇̃ + 𝜎̃ (S(u|𝛘,ξ)-S(0.5|𝛘,ξ))/(S(0.75|𝛘,ξ)-S(0.25|𝛘,ξ))
    
    f(u|𝜎̃,𝛘,ξ) =  (S(0.75|𝛘,ξ)-S(0.25|𝛘,ξ))/(𝜎̃ d/du S(u|𝛘,ξ)) where
    d/du S(u|𝛘,ξ) = u^(𝛼+𝛽−1) + (1−u)^(𝛼−𝛽−1) where
    𝛼 = 0.5 (0.5-ξ)/(sqrt(ξ(1-ξ))
    𝛽 = 0.5 (𝛘)/(sqrt(1-𝛘^2))
    
    
    ----------------------------------------
    References:
    1. Chalabi, Y., Scott, D.J., & Wuertz, D. 2012. Flexible distribution modeling with the generalized lambda distribution. 
    2. Freimer, M., Kollia, G., Mudholkar, G.S., & Lin, C.T. 1988. A study of the
        generalized Tukey lambda family. Communications in Statistics-Theory and Methods, 17, 3547–3567.
    3. S. Su. A discretized approach to flexibly fit generalized lambda distributions to data. Journal of Modern Applied Statistical Methods, 4(2):408–424, 2005.
    ----------------------------------------
    """
    
    def __init__(self, data):
        self._data = np.array(data).ravel()
        self._max_val = np.sort(self._data)[-1]
        
    def get_params(self,initial_guess=(-0.514,0.337), method='robust_moments_matching', 
                       tol = 1e-5, disp_fit= True, disp_gof=True,  bins_gof = 9, random_state= None,**kwargs):
        """ Outputs parameters of estimated GLD distribution for data in CSW paramterization,section 4, Chalabi et al 2012
        
        Args:
            initial_guess (array-like) : The initial guess is for shape parameters, chi and xi (𝛘 and ξ)
                Refer to Figures 14, Chalabi et al 2012, for different sets of shape parameters
                initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1) 
            method (str) : Various methods to estimate parameters, section 4, Chalabi et al 2012:
                1. Robust Moments Matching (robust_moments_matching)
                2. Histogram Approach (histogram_approach)
                3. Goodness of Fit approaches (goodness_of_fit)
                4. Quantile Matching  (quantile_matching)
                5. Maximum log-likelihood estimation (max_log_likelihood)
                6. Maximum product of spacing estimation (max_product_spacing)
                The default is robust_moments_matching. 
                Note: The method for trimmed l-moments is not defined in this class. 
            tol (float) : Tolerance for termination of the selected minimization algorithm.
            disp_fit (bool) : Plots PDF, CDF and Q-Q plot to visualize fit
            disp_gof (bool) : Prints goodness of fit test results 
            bins_gof (int) : Number of bins to divide data to calculate counts of expected values
            random_state (None or int), optional : The seed of the pseudo random number generator. The default is None.
            bin_method (str) : Three methods for calculating number of histogram bins, section 3.5
                1. Sturges breaks (sturges)
                2. Scott breaks (scott)
                3. Freedman-Diaconis breaks (freedman-diaconis) 
                Default value is  Freedman-Diaconis breaks
            statistic (str) : Test statistic to use for goodness of fit approach, section 4.3
                1. Kolmogorov-Smirnov Statistic (kstest)
                2. Cramér–von Mises (cramervonmises)
                3. Anderson-Darling Statistic (anderson_darling)
                Default value is Kolmogorov-Smirnov Statistic 
            n (int) : Input variable for quantile matching method estimation
                It is cardinality of p where p is an indexed set of probabilities in range 0-1 . Default value is 100
        
        Returns:
            Array of location, scale, asymmetry and steepness parameters in CSW Paramterization (Median, InterQuartile Range, Chi, Xi) 
            if disp_fit is set to True , plots distribution function fit to data   
            if disp_gof is set to True , shows goodness of fit test values
        """
        bin_method = kwargs.get('bin_method',"freedman-diaconis")
        statistic = kwargs.get('statistic',"kstest")
        n= kwargs.get('n',100)
        initial_guess = np.array(initial_guess)
        # median
        median = self._pi(self._data,0.5)
        # interquartile range
        iqr = self._interquartile_range(self._data)
        # chi and xi
        if method=='robust_moments_matching':
            chi,xi = self._robust_moments_chi_xi(self._data,initial_guess, tol)
        elif method=='histogram_approach':
            chi,xi = self._histogram_approach_chi_xi(self._data, initial_guess,tol, bin_method)
        elif method == 'goodness_of_fit':
            chi,xi = self._goodness_of_fit_approach_chi_xi(self._data,initial_guess,tol, statistic)
        elif method == 'quantile_matching':
            chi,xi = self._quantile_matching_approach_chi_xi(self._data,initial_guess,tol,n)
        elif method == 'max_log_likelihood':
            chi,xi = self._maximum_likelihood_approach_chi_xi(self._data,initial_guess,tol)    
        elif method == 'max_product_spacing':
            chi,xi = self._maximum_product_of_spacing_approach_chi_xi(self._data,initial_guess,tol)      
        else:
            raise ValueError('Parameter Estimation Method not valid')

        params =  [median, iqr, chi, xi]
        np.set_printoptions(legacy='1.25')
        print("CSW params: ", params)
    
        # Goodnesss of fit tests 
        if disp_gof:
            ks, chi2 = self._gof_tests(self._data, params,bins_gof)
            print('')
            print('Goodness-of-Fit')
            print(ks)
            print(chi2)
        
        # plot to see how good the GLD fit is to data
        if disp_fit:
            self.fit_plot(params,method)
        return params
    
    def fit_plot(self,params,method, ):
        """ Plots to display fitted GLD with data
        
        Args:
            params (array like): Params in CSW Paramterization
            method (str): Method used to find chi and xi
        
        Returns:
            3 plots on same axis : PDF, CDF and Q-Q plot with title stating the method to estimate parameters
        """
        
        plt.rcParams.update({'font.size': 14})
        fig,ax = plt.subplots(1,3,figsize = (15,5))
        # pdf
        ax[0].hist(self._data,bins=  self._hist_nbins(self._data, 'freedman-diaconis'),
                    density = True,color = 'skyblue')
        u_array = np.linspace(0.001,0.999,100)
        ax[0].plot(self._Q(params,u_array),self.pdf(params,u_array),lw = 2,color = 'r')
        ax[0].set_title('PDF', fontsize=18)
        ax[0].grid()
        # cdf
        ax[1].plot(np.sort(self._data), np.arange(len(self._data))/len(self._data),color = 'skyblue',lw = 2)
        ax[1].plot(self._Q(params,u_array),u_array, color= 'r')
        ax[1].grid()
        ax[1].set_title('CDF', fontsize=18)
        x = np.sort(self._data)
        y = (np.arange(len(self._data))+0.5)/len(self._data)        
        # q-q plot
        ax[2].plot(self._Q(params,y), x,'bo',ms = 3)
        m1 = np.min([x,self._Q(params,y)])
        m2 = np.max([x,self._Q(params,y)])
        ax[2].plot([m1,m2], [m1,m2],'r')
        ax[2].grid()
        ax[2].set_title('Q-Q-plot') 
        fig.suptitle(f"GLD {method} Fit on data",fontsize=22)
        plt.tight_layout()
        plt.show() 
    
    def generate_sample(self,params,n,m=1,random_state = None, disp_fit= True, disp_qq= True):
        """ Generates samples of size (n,m) from a GLD distribution 
        defined by its parameters (params)
        
        Args:
            params (array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            n (int) : Number of points in sample data
            m (int), optional : generates 2D sample array. default value of m is 1 for 1d array. 
            random_state (None or int), optional : The seed of the pseudo random number generator. Default is set to None.
            disp_fit (bool) : if True, displays distribution of data using a probability density curve
            disp_qq (bool) : if True, generates a probability plot of sample data against the quantiles of Normal Distribution
        Returns:
            Array of size (n,m)
            PDF and quantile-quantile plot if set to True
        """
        # u_array random floats in the half-open interval [0.0, 1.0)
        rng = np.random.default_rng(seed=random_state)
        if m>1:
            u_array = rng.random((n,m))
        else:
            u_array = rng.random((n,))
        sample_array = np.array([self._Q(params, u) for u in u_array])
        if disp_fit:
            self._display_fit(params,sample_array)
        if disp_qq:
            plt.figure(figsize=(12,9))
            stats.probplot(sample_array, dist='norm', plot=plt)
            plt.title('Q-Q Plot of Data', fontsize=16)
            plt.show()   
        return sample_array 
        
    def VaR(self,params,u):
        """ outputs Value-at-Risk at probability u
        maximum loss forecast that may happen with 
        probability u ∈ [0,1] over the holding period
        section 5.2, Chalabi et al 2012
        
        Args:
            params(array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            u (float) : Lower tail probability, must be between 0 and 1.
        
        Returns :
            Value at Risk with specified probability over the holding period
 
        """
        if self._check_params(params):
            pass
        else:
            raise ValueError('CSW Parameters are not valid')
        return self._Q(params,u)

    def ES(self,params,u):
        """ outputs Expected Shortfall - average VaR over the interval [0,u]
        section 5.2, Chalabi et al 2012
        
        Args:
            params(array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            u (float) : Lower tail probability, must be between 0 and 1.
        
        Returns:
            Expected Shortfall with specified probability over the holding period

        """
        if self._check_params(params):
            median, iqr, chi, xi = params
        else:
            raise ValueError('CSW Parameters are not valid')

        A = iqr/(self._s_function(3/4,chi, xi)-self._s_function(1/4,chi, xi))
        B = -1/(self._s_function(3/4,chi, xi)-self._s_function(1/4,chi, xi))
        a = self._alpha(xi)
        b = self._beta(chi)

        if chi == 0 and xi == 0.5:
            es =  u*(B+median+A*np.log(u))+ (A-A*u)*np.log(1-u)
        elif chi!=0 and xi==(1+chi)/2 :
            es = B*u + A*(((1-u)**(1+2*a)-1)/2*a + 4*a**2) + A*u*((1/(2*a)) + np.log(u)-1) + u*median
        elif chi!=0 and xi== (1-chi)/2:
            es =  ((A-A*u)*np.log(1-u)) + u*(B+median) + (A*u*(-1+4*b**2+u**(2*b)))/(2*b*(1+2*b))
        else:
            es =   -((u*median) + (A*u*(1+a+b))/((a+b)*(1+a+b)) - (A*u)/(a+b) + (A*u)/(a-b) +B*u + (A*((1-u)**(1+a)-(1-u)**b)*(1-u)**(-b))/((a-b)*(1+a-b)))
        return es
    
    def plot_pdf(self,params_list, disp_data= True, ymin= 0.001, ymax= 0.999, n_points= 100 , bins= None, names= None, color_emp = 'lightgrey', colors = None):
        """ Plot probability density functions of GLD.
        Helps compare various  GLD probability density functions with different parameters
        against empirical data represented by histogram.

        Args:
            params_list (list) : list of CSW params defined by various methods
            disp_data (bool) : Plots histogram of empirical data
            ymin (float, optional): lower probability. Defaults to 0.01.
            ymax (float, optional): Upper probability.  Defaults to 0.99.
            n_points (int, optional): Number of points for plotting pdf. Defaults to 100.
            bins (int, optional): Number of bins for plotting histogram.  Defaults to None.
            names (sts list , optional):Names of labels for the legend. Length of the list should be equal to the length of param_list.  The default is None.
            color_emp (str, optional): Color of the histogram. Defaults to 'lightgrey'
            colors (str list ,optional): Line colors of PDFs. Length of the list should be equal to the length of param_list. Defaults to None
        
        Returns: 
            Plots PDF using params from various methods
        """
        param_list = np.array(params_list)
        if param_list.ndim==1:
            param_list = param_list.reshape(1,-1)
        if names is None:
            names = [str(x) for x in param_list]
        if colors is None:
            colors = [None]*len(param_list)
        plt.figure()
        plt.grid()
        pdf_max = 0
        if disp_data:
            p = plt.hist(self._data,bins = bins, color = color_emp, density = True)
            pdf_max = np.max(p[0])
        y = np.linspace(ymin,ymax,n_points)
        for i in range(len(param_list)):
            param = param_list[i]
            plt.plot(self._Q(param, y ), self.pdf(param, y), color = colors[i])
            pdf_max = np.max([pdf_max,np.max(self.pdf(param, y))])
        plt.ylim(ymin = 0,ymax = pdf_max * 1.05)
        plt.legend(names,bbox_to_anchor=(1.0,  1.0 ))
        plt.title('PDF') 
        plt.show()
    
    def plot_cdf(self,params_list, disp_data= True, ymin= 0.001, ymax= 0.999 , n_points= 100, names= None, color_emp = 'lightgrey', colors = None):
        """ Plot cumulative distribution functions of GLD.
        Helps compare various  GLD cumulative density functions with different parameters
        against empirical data represented by histogram.
        
        Args:
            params_list (list) : list of CSW params defined by various methods
            disp_data (bool) : Plots empirical cumulative distribution.
            ymin (float, optional): lower probability. Defaults to 0.01.
            ymax (float, optional): Upper probability.  Defaults to 0.99.
            n_points (int, optional): Number of points for plotting cdf. Defaults to 100.
            names (sts list , optional):Names of labels for the legend. Length of the list should be equal to the length of param_list.  The default is None.
            color_emp (str, optional): Color of the histogram. Defaults to 'lightgrey'
            colors (str list ,optional): Line colors of PDFs. Length of the list should be equal to the length of param_list. Defaults to None
        
        Returns: 
            Plots CDF using params from various methods
        """
        param_list = np.array(params_list)
        if param_list.ndim==1:
            param_list = param_list.reshape(1,-1)
        if names is None:
            names = [str(x) for x in param_list]
        if colors is None:
            colors = [None]*len(param_list)
        plt.figure()
        plt.grid()
        if disp_data:
            ordered_data = np.sort(self._data)
            steps= np.arange(len(self._data))/len(self._data)
            plt.plot(ordered_data, steps, color= color_emp, lw= 2)
            names= np.hstack(['empirical data', names ])
        y = np.linspace(ymin,ymax,n_points)
        for i in range(len(param_list)):
            param = param_list[i]
            plt.plot(self._Q(param, y ),  y,color = colors[i])
        plt.ylim(ymin = 0)
        plt.legend(names,bbox_to_anchor=(1.0,  1.0 ))
        plt.title('CDF')
        plt.show()  
    
    def cdf_x(self,params,x,tol = 1e-6 ):
        """ Calculates Cumulative distribution function (F_CSW) of GLD at value/ array of x 
        F_csw[Q_csw(u)] = u for all u∈[0,1]
        CDF at x is found numerically by 
        finding a local minimizer of the scalar function find_cdf_cost 
        in the interval 0 < u_optimal < 1 using Brent’s method
        
        Args:
            params (array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            x (float) : A value from GLD for which probability that the random variable X is less than or equal to x
                F(x)=Pr[X≤x]
                
        Raises:
            ValueError: if csw parameters are not valid.        
        
        Returns:
            float, array-like
            Note: output between 0 and 1. 
        """
        def find_cdf_cost(u):
            """
            cost function that needs to be minimized
            to estimate u - lower tail probability
            """
            return np.square(self._Q(params,u)-x_arg)

        if self._check_params(params):
            median, iqr, chi, xi = params
        else:
            raise ValueError('CSW Parameters are not valid')
            
        min_val,max_val= self._params_support(params)
        x= np.array([x]).ravel()
        # start cdf result with na
        result_cdf = x*np.nan
        result_cdf[x<min_val] = 0
        result_cdf[x>max_val] = 1
        index_mask = np.argwhere(np.isnan(result_cdf)).ravel()
        for i in index_mask:
            x_arg = x[i]

            result_cdf[i] = fminbound(find_cdf_cost, x1=0,x2=1,
                                       xtol=tol)
        return result_cdf
    
    def pdf_x(self,params,x):
        """ Calculates Probability distribution function (f_CSW) 
        of GLD at value/ array of x numerically
        
        Args:
            params (array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            x (float) : A value from GLD for which probability that the random variable X is equal to x
                Pr[X=x]
        
        Returns:
            float, array-like
            Note: output between 0 and 1
        """
        u = self.cdf_x(params,x)
        result_pdf = self.pdf(params, u)
        min_val,max_val= self._params_support(params)
        result_pdf[np.logical_or(x<min_val, x>max_val)] = 0
        return result_pdf
    
    def qdf(self,params, u):
        """ outputs the quantile density function at u of GLD
        q(u) = Q'(u), derivative of Quantile function Q_csw
        domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
        eq 11, Chalabi et al 2012
        
        Args:
            params (array-like): Parameters of GLD in CSW Parametrization. Obtained from function get_params
            u (float) : Lower tail probability, must be between 0 and 1.
        
        Returns:
            float, array-like
        """
        median, iqr, chi, xi = params
        d_du = self._first_derivative_s_function(u,chi,xi)
        qdf = iqr/(self._s_function(3/4,chi, xi)-self._s_function(1/4,chi, xi))*d_du
        return qdf 
    
    def pdf(self,params, u):
        """ outputs the density quantile function at u of GLD
        fQ(u) = 1/q(u)
        domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
        eq 10, Chalabi et al 2012
        
        Args:
            params (array-like): Parameters of GLD in CSW Parametrization. Obtained from function get_params
            u (float) : Lower tail probability, must be between 0 and 1.
        
        Returns:
            float, array-like
        """
        return 1/self.qdf(params, u)
    
    def _Q(self,params,u):
        """ Quantile Distribution Function (Q_CSW) of the GLD in the CSW parameterization
        outputs the value of a random variable X such that the probability of X is less than or equal to u
        
        P(X< Q_CSW(u)) = u ∀u∈[0,1]
        where Q_CSW(u) is the quantile function,
        X - random variable, and 
        lower tail probability value u
        eq 9 , Chalabi et al 2012
        
        Args:
            params (array-like): Parameters of GLD in CSW Parametrization. Obtained from function get_params
            u (float) : Lower tail probability, must be between 0 and 1.
        
        Raises :
            Value Error : if csw parameters are not valid
            Value Error : if tail probability is outside [0,1]
            
        Returns:
            float, array-like
        """ 
        u = np.array(u).astype(float)
        if np.logical_or(u>1, u<0).any(): 
            raise ValueError('u should be in range [0,1]')
        if self._check_params(params):
            median, iqr, chi, xi = params
        else:
            raise ValueError('CSW Parameters are not valid')
        numerator = self._s_function(u,chi, xi)-self._s_function(1/2,chi, xi)
        denominator = self._s_function(3/4,chi, xi)-self._s_function(1/4,chi, xi)
        X= median + iqr*numerator/denominator
        return X
    
    def _check_params(self,params):
        """ Checks if parameters are valid within CSW Parameterization 
        Conditions to check:
        1. There are 4 params - median, iqr, chi, xi
        2. chi(𝛘) ∈ (-1,1) and xi(ξ) ∈ (0,1)
        
        Args:
            params (array-like): Parameters of GLD in CSW Parametrization. Obtained from function get_params
        
        Raises: 
            ValueError: when one or more conditions aren't met 
            
        Returns:
            True, False or ValueError
        """
        if len(params)!=4:
            raise ValueError('GLD has 4 parameters')            
        if not np.isfinite(params).all():
            return False
        if -1<=params[2]<=1 and 0<=params[3]<=1 :
            return True

    def _params_support(self,params, eps= 0.0001):
        """ outputs value bounds of GLD defined by params
        Minimum and Maximum possible values of GLD with specified CSW Parameters
        
        Args:
            params (array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            eps (float,optional ): Parameter of support fitting. Tail probability of minimum and maximum data points. The default is 0.0001.
            
        Returns :
            Array of length 2. 
        """
        min_val = self._Q(params,eps)
        max_val = self._Q(params,1-eps)
        return min_val, max_val 

    def _gof_tests(self, array, params,bins_gof):
        """ Perform two Goodness-of_Fit tests
        1. Kolmogorov-Smirnov test  
        2. one-way chi-square test from scipy.stats
        
        Args:
            array (array-like): data fro which goodness of fits are calculated
            params (array-like): Parameters of GLD in CSW Parametrization. Obtained from function get_params
            bins_gof (int): Number of bins to divide data to calculate counts of expected values
        
        Returns:
            Test statistic and respective p values for Kolmogorov-Smirnov test and chi-square test
        """
        def cdf(x):
            """Auxiliary function for goodness of fit test."""            
            return self.cdf_x(params,x)
    
        def chisquare_test(array,params, bins_gof ):
            u_array = np.linspace(0.00001, 0.999999, bins_gof +1 )
            f_obs = np.histogram(array,np.array([self._Q(params,u) for u in u_array]) )[0]
            f_exp = np.array([len(array)/bins_gof]*bins_gof ).astype(int)
            # chi-squared test for goodness of fit requires the sums of both inputs to be (almost) the same
            f_exp = np.sum(f_obs)/np.sum(f_exp) * f_exp
            chi2 = stats.chisquare(f_obs,f_exp)
            return chi2
        
        # Kolmogorov-Smirnov test
        ks= stats.kstest(array, cdf)
        # Chi-squared test
        chi2 = chisquare_test(array, params, bins_gof )
        return ks, chi2
    
    def _robust_moments_chi_xi(self,array,initial_guess,tol):
        """  Robust Moments matching approach to estimate GLD distribution shape parameters
        Approach: Moments are replaced with robust quantile-based measures. Median instead 
        of mean. Interquartile Range (IQR) instead of variance. Skewness and kurtosis based 
        on percentiles rather than higher-order moments. Solve nonlinear system of equations 
        with two unknowns (chi and xi). The population robust skewness and robust kurtosis 
        are equated with robust skewness ratio of Bowley and robust kurtosis ratio of Moors. 
        Section 4.1 , Chalabi et al 2012
        
        Args:
            array (array-like) : data for which chi and xi parameters are estimated
            initial_guess (array-like) : initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
            tol (float), optional : Tolerance for termination of the selected minimization algorithm.
        
        Returns :
            Array of asymmetry and steepness parameters in CSW Paramterization (Chi, Xi)
        """
        # empirical quantile based measures
        skew= self._bowley_skewness_ratio(array)
        kurt= self._moor_kurtosis_ratio(array)

        def cost_function(sol):
            chi,xi = sol
            return np.array([(self._population_skewness(chi,xi)-skew), (self._population_kurtosis(chi,xi)-kurt)])
        # np.abs(self._population_skewness(chi,xi)-skew)+ np.abs(self._population_kurtosis(chi,xi)-kurt)])
        res = least_squares( cost_function, initial_guess, bounds=([-1,0],[1,1]) )
        # minimize(cost_function, x0=initial_guess, method= 'L-BFGS-B', bounds= ((-1,1),(0,1)), tol= tol)  
        return res.x

    def _histogram_approach_chi_xi(self,array, initial_guess,tol,bin_method):
        """ Histogram Approach to estimate GLD distribution shape parameters
        Approach: The empirical data is binned into a histogram and resulting probabilities, taken to be 
        at the midpoints of the histogram bins are fitted to the true GLD density. 
        Three methods for choosing approporiate number of bins:
        1. Sturges breaks (sturges)
        2. Scott breaks (scott)
        3. Freedman-Diaconis (freedman-diaconis)
        Section 4.2 , Chalabi et al 2012
        Args:
            array (array-like) : data for which chi and xi parameters are estimated
            initial_guess (array-like) : initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
            tol (float), optional : Tolerance for termination of the selected minimization algorithm.
            bin_method (str) : one of the three binning methods. default method is freedman-diaconis
        
        Returns:
            Array of asymmetry and steepness parameters in CSW Paramterization (Chi, Xi) 
        """
        bin_width, bin_midpoints, proportion= self._get_hist_patches(array,bin_method)     
        median = self._pi(array,0.5)
        iqr = self._interquartile_range(array)

        def cost_function(sol):
            """
            cost function that needs to be minimized
            to estimate chi and xi 
            """
            chi,xi = sol
            params = median, iqr, chi, xi 
            GLD_proportion = []
            for i in bin_midpoints:
                # proportion of data at point i from theoretical GLD distribution
                proportion_i = self.pdf_x(params,i)*bin_width
                GLD_proportion.append(proportion_i)
            GLD_proportion = np.array(GLD_proportion).ravel()
            return (proportion*(np.square(proportion-GLD_proportion))).sum()
        res = minimize(cost_function,method="L-BFGS-B", x0=initial_guess,
                       bounds= ((-1,1),(0,1)),tol= tol)  
        return res.x
    
    def _goodness_of_fit_approach_chi_xi(self,array,initial_guess,tol, statistic):
        """Goodness of fit approach to estimate GLD distribution shape parameters.
        Approach: Use statistic based on empirical distribution to measure difference between 
        hypothetical GLD distribution and the empirical distribution and attempt to minimize it.
        Statitics :
            1. Kolmogorov-Smirnov Statistic (kstest)
            2. Cramér–von Mises (cramervonmises)
            3. Anderson-Darling Statistic (anderson_darling)
            Default value is Kolmogorov-Smirnov Statistic 
        Section 4.3 , Chalabi et al 2012
        
        Args:
            array (array-like) : data for which chi and xi parameters are estimated
            initial_guess (array-like) : initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
            tol (float), optional : Tolerance for termination of the selected minimization algorithm.
            statistic (str) : Test statistic to use for goodness of fit approach, section 4.3

        Returns:
            Array of asymmetry and steepness parameters in CSW Paramterization (Chi, Xi) 
        """
        median = self._pi(array,0.5)
        iqr = self._interquartile_range(array)
        
        def cost_function(sol):
            """
            cost function that needs to be minimized
            to estimate chi and xi 
            """
            chi,xi = sol
            params = median, iqr, chi, xi
            if not self._params_support(params):
                raise ValueError("Params not in support")
                # return self._max_val
            def cdf(x):
                """Auxiliary function for goodness of fit test."""            
                return self.cdf_x(params,x)
            if statistic == 'kstest':
                # Kolmogorov-Smirnov test
                ks= stats.kstest(array, cdf)
                return ks.statistic
            elif statistic == 'cramervonmises':
                # Cramér-von Mises test
                c = stats.cramervonmises(array,cdf)
                return c.statistic 
            elif statistic == 'anderson_darling':
                # Anderson-Darling test
                ad = self._anderson_darling_statistic(array,params)
                return ad
            else:
                raise ValueError('Goodness of Fit Approach not valid. Specify one of the following: kstest,cramervonmises,anderson_darling ')
        res = minimize(cost_function,method="L-BFGS-B", x0=initial_guess,
                    bounds= ((-1,1),(0,1)),tol= tol)
                  
        return res.x
    
    def _quantile_matching_approach_chi_xi(self,array,initial_guess,tol,n):
        """ Quantile Matching approach to estimate GLD distribution shape parameters.
        Approach: Find parameter values (chi and xi) that minimize the difference between 
        the theoretical and sample quantiles. To assess the fit, an error function E is used,  
        the sum of squared differences between empirical and theoretical quantiles at specified probabilities p
        
        Args:
            array (array-like) : data for which chi and xi parameters are estimated
            initial_guess (array-like) : initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
            tol (float), optional : Tolerance for termination of the selected minimization algorithm.
            n (int): It is cardinality of p where p is an indexed set of probabilities in range 0-1 . Default value is 100

        Returns:
            Array of asymmetry and steepness parameters in CSW Paramterization (Chi, Xi) 
        """
        
        median = self._pi(array,0.5)
        iqr = self._interquartile_range(array)
           
    
        def cost_function(sol):
            """
            cost function that needs to be minimized
            to estimate chi and xi 
            """
            chi,xi = sol
            params = median, iqr, chi, xi
            u_array = np.linspace(0.000001,0.999999,n)
            theoretical = np.array([self._Q(params, u) for u in u_array])
            empirical = np.array([np.quantile(a=array, q=u) for u in u_array])
            return empirical- theoretical  
        res = least_squares(cost_function, x0=initial_guess, bounds= ([-1,0],[1,1]) )
                    
        return res.x 
    
    def _maximum_likelihood_approach_chi_xi(self,array,initial_guess,tol):
        """ Maximum log-likelihood approach to estimate GLD distribution shape parameters.
        Approach : For a random sample of n observations drawn from probability distribution with parameter set (CSW parameters), 
        the value of log-likelihood function is maximized to obtain the parameters.
        
        The log-likelihood function for a distribution "f(x)" is given by the expression:
        ln(L(θ)) = ∑ ln(f(x_i | θ)) where
        where "θ" represents the parameter(s) of the distribution, 
        "x_i" are the individual data points the sample, 
        "f(x_i | θ)" is the probability density function (PDF) of the distribution evaluated at each data point, and 
        "ln" denotes the natural logarithm function; 
        essentially, it is the sum of the natural logarithm of the likelihood of each data point given the parameter(s) "θ"
        
        Args:
            array (array-like) : data for which chi and xi parameters are estimated
            initial_guess (array-like) : initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
            tol (float), optional : Tolerance for termination of the selected minimization algorithm.

        Returns:
            Array of asymmetry and steepness parameters in CSW Paramterization (Chi, Xi) 
        """
        median = self._pi(array,0.5)
        iqr = self._interquartile_range(array)
        
        def log_likelihood(sol):
            """
            Likelihood cost function that needs to be minimized
            to estimate chi and xi 
            """
            chi,xi = sol
            params = median, iqr, chi, xi   
            if not self._params_support(params):
                return self._max_val    
            return -np.sum(np.log(self.pdf_x(params, array)))
        res = minimize(log_likelihood, x0=initial_guess, method= 'Nelder-Mead', bounds= ((-1,1),(0,1)),
                        tol= tol)  
        return res.x
    
    def _maximum_product_of_spacing_approach_chi_xi(self,array,initial_guess,tol):
        """ Maximum log-likelihood approach to estimate GLD distribution shape parameters.
        Approach : The random variates of continuous distribution are transformed to variables of uniform distribution.
        The parameter estimates are values that make the spacings between cumulative distribution functions of the random variates equal. 
        Equivalent to maximizing the geometric means of the probability spacings.

        Args:
            array (array-like) : data for which chi and xi parameters are estimated
            initial_guess (array-like) : initial_guess to be within domains of shape parameters 𝛘 ∈ (-1,1) and ξ ∈ (0,1)
            tol (float), optional : Tolerance for termination of the selected minimization algorithm.

        Returns:
            Array of asymmetry and steepness parameters in CSW Paramterization (Chi, Xi) 
        """
        median = self._pi(array,0.5)
        iqr = self._interquartile_range(array)
        array = np.sort(array)
        
        def maximum_product_of_spacing(sol):
            """
            Spacing cost function that needs to be minimized
            to estimate chi and xi 
            """
            chi,xi = sol
            params = median, iqr, chi, xi   
            if not self._params_support(params):
                return self._max_val   
            return -np.mean(np.log(np.abs(np.diff(self.cdf_x(params,array)))))
        res = minimize(maximum_product_of_spacing, x0=initial_guess, method= 'Nelder-Mead', bounds= ((-1,1),(0,1)),
                        tol= tol)  
        return res.x
    
    def _pi(self,array,q,method='midpoint'):
        """ returns q-th quantile of the array input data
        
        Args:
            array (array-like) : data for which qth quantile is calculated
            q (float, array-like) : quantile values, such as 0.25, 0.5, 0.75,0.9, etc
            method (str) :method to use for estimating the quantile.  
                other numpy methods available, numpy default -'linear'
        
        Returns:
            float, array-like        
        """
        return np.quantile(a=array, q=q, method=method)

    def _interquartile_range(self,array):
        """ outputs interquartile range of input array
        difference between values at 75th and 25th percentile
        Interquartile range = Q(0.75) - Q(0.25)
        
        Args:
        array (array-like) : data array for which interquantile range is calculated
        
        Returns:
            float, array-like  
        """
        return  self._pi(array,q=0.75)-self._pi(array,q=0.25)

    def _alpha(self,xi):
        """ helper function for _s_function 
        𝜉 -> xi
        eq 7a ,Chalabi et al 2012
        
        Args:
            xi (float) : shape parameter of CSW parametrization
        
        Returns:
            float, array-like  
        """
        return (0.5*((0.5-xi)/(math.sqrt(xi*(1-xi)))))

    def _beta(self,chi):
        """ helper function for _s_function 
        𝜒 -> chi 
        eq 7b , Chalabi et al 2012
        
        Args:
            chi (float) : shape parameter of CSW parametrization
        
        Returns:
            float, array-like 
        """
        return (0.5*chi/math.sqrt(1-chi**2))
    
    def _s_function(self,u,chi, xi):
        """ The S function S(u|𝜒,𝜉) in terms of shape parameters 𝜒,𝜉
        probability u obtained from quantile based estimators
        used within quantile function of GLD in CSW Parametrization
        eq 8, Chalabi et al 2012
        𝜒 -> chi 
        𝜉 -> xi

        Args:
            u (float): Lower tail probability, must be between 0 and 1.
            chi (float): shape parameter of CSW parametrization
            xi (float): shape parameter of CSW parametrization

        Raises:
            ValueError: if u isn't in range 0-1 inclusive

        Returns:
            float, array-like
        
            
        """
        a = self._alpha(xi)
        b = self._beta(chi)
        
        if np.logical_and(u>0, u<1).all():
            if chi == 0 and xi == 0.5:
                return np.log(u) - np.log(1-u)
            elif chi!=0 and xi==(1+chi)/2 :
                return np.log(u)- ((((1-u)**(2*a))-1)/(2*a))
            elif chi!=0 and xi== (1-chi)/2:
                return (((u**(2*b))-1)/(2*b))- np.log(1-u)
            else:
                return (((u**(a+b))-1)/(a+b)) - (((1-u)**(a-b))-1)/(a-b)
        elif u==0:
            if xi < (1+chi)/2:
                return -1/(a+b)
            else: 
                return -np.inf
        elif u==1:
            if xi < (1-chi)/2:
                return 1/(a-b)
            else:
                return np.inf
        else:
            raise ValueError("u has to be in range [0,1] inclusive")
    
    def _first_derivative_s_function(self,u,chi,xi):
        """ calculates derivative of _s_function d/du S(u|𝜒,𝜉)

        Args:
            u (float): Lower tail probability, must be between 0 and 1.
            chi (float): shape parameter of CSW parametrization
            xi (float): shape parameter of CSW parametrization

        Returns:
            float, array-like
        """
        a = self._alpha(xi)
        b = self._beta(chi)
        return (u**(a+b-1)+(1-u)**(a-b-1))

    
    def _bowley_skewness_ratio(self,array, method='midpoint'):
        """ robust skewness ratio of Bowley(1920)

        Args:
            array (array-like): data for which Bowley skewness ratio is estimated
            method (str, optional): numpy quantile method . Defaults to 'midpoint'.

        Returns:
            float
        """
        s = (self._pi(array,3/4)+self._pi(array,1/4)-(2*self._pi(array,2/4)))/(self._pi(array,3/4)-self._pi(array,1/4))
        return s

    def _moor_kurtosis_ratio(self,array,method='midpoint'):
        """ robust Kurtosis ratio of Moor

        Args:
            array (array-like): data for which Moor kurtosis ratio is estimated
            method (str, optional): numpy quantile method. Defaults to 'midpoint'.

        Returns:
            float
        """

        k = (self._pi(array,7/8)-self._pi(array,5/8)+self._pi(array,3/8)-self._pi(array,1/8))/(self._pi(array,6/8)-self._pi(array,2/8))
        return k
    
    def _population_skewness(self,chi,xi):
        """  population robust skewness
        eq 16(a) Chalabi et al 2012

        Args:
            chi (float): shape paramter of CSW parametrization
            xi (float): shape paramter of CSW parametrization

        Returns:
            float
        """

        return (self._s_function(3/4,chi, xi)+self._s_function(1/4,chi, xi)-2*self._s_function(2/4,chi, xi))/(self._s_function(3/4,chi, xi)-self._s_function(1/4,chi, xi))

    def _population_kurtosis(self,chi,xi):
        """ population robust kurtosis
        eq 16(b) Chalabi et al 2012
        
        Args:
            chi (float): shape paramter of CSW parametrization
            xi (float): shape paramter of CSW parametrization

        Returns:
            float
        """
        return (self._s_function(7/8,chi, xi)-self._s_function(5/8,chi, xi)+self._s_function(3/8,chi, xi)-self._s_function(1/8,chi, xi))/(self._s_function(6/8,chi, xi)-self._s_function(2/8,chi, xi))
    
    def _hist_nbins(self,array, bin_method):
        """ Calculates number of bins for data array
        1. Sturges breaks (sturges)
        2. Scott breaks (scott)
        3. Freedman-Diaconis breaks (freedman-diaconis)
        
        Args:
            array (array-like): data for which number of bins is calculated
            bin_method (str): methods for calculating number of histogram bins

        Raises:
            ValueError: if bin_method doesn't match one of the three methods specified

        Returns:
            int 
        """
        n= len(array)
        max_val = np.max(array)
        min_val = np.min(array)

        if bin_method == 'sturges':
            n_bins= np.ceil(math.log2(n+1)).astype(int)
        elif bin_method == 'scott':
            sd = np.std(array)
            if  sd ==0:
                n_bins = 1
            else:
                h= 3.49* sd*n**(1/3)
                n_bins = np.ceil((max_val-min_val)/h).astype(int)
        elif bin_method == 'freedman-diaconis':
            iqr = self._interquartile_range(array)
            if iqr == 0:
                h= stats.median_abs_deviation(array)
            else:     
                h = iqr/n**(1/3)
            n_bins = np.ceil((max_val-min_val)/h).astype(int)
        else:
            raise ValueError("Specify method to determine the number of bins")
        return n_bins
    
    def _get_hist_patches(self,array, bin_method):
        """ helper function for histogram approach of finding CSW Parameters

        Args:
            array (_type_): data for histogram approach is used
            bin_method (str): bin_method can either be sturges, scott or freedman-diaconis

        Returns:
            outputs bin width, bin midpoints and proportions for each
        """
        n_bins = self._hist_nbins(array, bin_method)
        (counts, bins, patches) = plt.hist(array,cumulative=False, density=False, bins=n_bins)
        plt.title(f"Histogram with {n_bins} bins based on {bin_method} method")
        plt.ylabel("Counts")
        plt.xlabel("Data Range")
        proportion = counts/counts.sum()
        bin_width = bins[2]-bins[1]
        bin_midpoints = []
        for i in range(len(bins)-1):
            bin_mid = (bins[i] + bins[i+1])/2
            bin_midpoints.append(bin_mid)
        return bin_width, bin_midpoints, proportion 
    
    def _anderson_darling_statistic(self,array,params):
        """ Anderson-Darling statistic for optimization 

        Args:
            array (array-like): data for Anderson-Darling statistic is estimated
            params (array-like): Parameters of GLD in CSW Parametrization. Obtained from function get_params

        Returns:
            float
        """
          
        if not self._params_support(params):
            return self._max_val        
        u = self.cdf_x(params,array)
        ad_stat = -len(array) - 1/len(array)*np.sum((np.arange(1,len(array)+1)*2 - 1)*(np.log(u) + np.log(1 - u[::-1])))
        return ad_stat
    
    def _display_fit(self, sample_array):
        """ Plots the density plot of sample data generated from params using a probability density curve

        Args:
            params (array-like) : Parameters of GLD in CSW Parametrization. Obtained from function get_params
            sample_array : (array-like) : ample data generated from GLD    
            
        Returns:
            density plot     
        """
        fig, ax = plt.subplots(figsize=(7 ,5))
        sns.kdeplot(sample_array.ravel(), ax= ax, color='blue',label='GLD Sample')
        plt.title("Distribution of sample data generated from GLD parameters")
        plt.legend()
        plt.show()