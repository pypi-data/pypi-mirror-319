# 🛠️ dfhelper

## What is this?

Dfhelper is a versatile Python package that streamlines data preprocessing and visualization in Jupyter Notebooks. 
With intuitive functions for cleaning and transforming pandas DataFrames and the ability to render them as interactive 
HTML tables, this toolkit is an essential addition to any data scientist's arsenal. Simplify your data analysis process 
and gain clearer insights with dfhelper.

## Quick installation
```
!pip install dfhelper
```

## Main functionality
1) Output date frames in HTML. This is extremely useful when working with multiple selections
2) Output in HTML df.info() multiple dataframes
3) Output the size of the date frames in html.
4) The ability to display dataframes vertically and horizontally
5) Functions for summarizing the date of Ephraim, created for conducting EDA

## Quick Guide
```python
import pandas as pd
from dfhelper.viz import df_view, df_info_view, df_shape_view
from dfhelper.scout import summarize_df, summarize_dfs


# viz
df1 = pd.DataFrame(
            {"A": [1, 0, 0, None],
             "B": [1, 1, 2, 2],
             "C": [None, None, None, None]}
        )

df2 = pd.DataFrame(
            {"A": [1, 5, 0, 10],
             "B": [1, 1, 2, 2],
             "C": [None, 4, 16, 101]}
        )

# Output of two dataframes
df_view(df1, df2)
# Output information about two dataframes
df_info_view(df1, df2)
# Output of the sizes of two dataframes
df_shape_view(df1, df2)

# scount
# Table of the main characteristics of the dataframe
summarize_df(df1)
# Displaying the main characteristics of dataframes
summarize_dfs(df1, df2)
```

