

<h1>Cohort analysis </h1>

<p> Cohort is a group of people who share a common characteristic over a

certain period of time. Cohort Analysis is a study that focuses on activities of a

particular cohort. It allows us to identify relationship between characteristics of

a population and that population’s behaviour which can used in varying fields of

medicine, retail, ecommerce. It is a subset of behavioural analytics that takes the

data and rather than looking at all users as one unit, it breaks them into related

groups for analysis. </p>

<p> In our system, we

calculate the retention rate of customers where retention rate is the (No. of

customers - No. of customers who cancelled) of previous month / No. of

customers in the previous month. We use cohort analysis to observe what

happens to a group of customers that a join a particular time period say a

January 2015 cohort, February 2015 cohort etc. </p>

<h2>Data Manipulation </h2>

<p> The transactional data (purchase records) must me cleaned and grouped into cohorts. <a href="http://pandas.pydata.org/">Pandas </a> is used for this purpose.
<p><a href="http://matplotlib.org/">MatplotLib</a> is used to visualize the data, in the exploratory analysis process </p>

<h2>Interactive Web App </h2>
<p> In a Business scenario, communicating the insights gained from data, is as important as gaining the insights itself. We have a developed an interactive web app, which visualizes the data product-wise for the required timeline. </p>

<p><a href="http://bokeh.pydata.org/en/latest/">Bokeh</a> python package provides a good abstraction, which enables us to build data driven web-app with ease.

<p>use the following command from root-dir to launch the web-app </p>
```
bokeh serve --show cohort
```

![alt tag](https://github.com/gautham20/cohort-analysis/blob/master/cohort/data/results.png)

<p><i> green - 100% customer retention, red - 0% customer retention </i></p>
