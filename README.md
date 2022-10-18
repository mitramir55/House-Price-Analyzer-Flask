# House Price Analysis in Canada
![house](https://github.com/mitramir55/House-price-analysis/blob/main/static/assets/house-prices-scaled.jpg)

image source : [yourmoney.com](https://www.yourmoney.com/mortgages/house-prices-rise-at-fastest-pace-since-2007/)

### ⚙  How it works? 

**Note**: From November 2022, the app ([link](https://analyze-house-rentals.herokuapp.com/)) can only be run locally, since Heroku (previous server I used) has shut down its free
servers. 

*How to use*: clone the project, install Flask, and enter `flask run` in your terminal.

About the app:
On the index page, there are two options: try it, and preview
By selecting try it option, you will be sent to a page where you can specify all the 
variables of the data that will be collected. 
This dataset will be scraped from one of the ubiquitous renting websites (Rentfaster.com). 
Then it will be cleaned and filtered to give us records of individual residence options. 
The preprocessing steps are listed bellow.

A preview:
![image](https://user-images.githubusercontent.com/53291220/196306626-e6d486ff-777d-442f-a588-ca80cd74f475.png)

Choose the parameters:
![image](https://user-images.githubusercontent.com/53291220/196306655-68012b6f-38c9-42e4-a333-a24742b9a85f.png)


Sample of the analysis:

![image](https://user-images.githubusercontent.com/53291220/196307465-caaa45a1-b858-47c8-abdf-e1f18bb0452d.png)

See the corrolation in this type of housing:
![image](https://user-images.githubusercontent.com/53291220/196307634-e8aa20c8-332d-4687-a65d-e8732ce655c4.png)


### 🧹 Preprocessing

#### Filtering steps:

* removing the following columns (for protecting privacy of land owners):
`['phone', 'phone_2', 'f', 's', 'title', 'city','intro', 'userId','id', 'ref_id', 'email', 'v', 'thumb2', 'marker','preferred_contact']`

* filter out all the "Not Rented" records.
* dropping records with nulls in either the `price` or `sq_feet` column.



#### Conversions:

* separate utilities list (`utilities_included`) into separate columns. 
* separate records which include more than one residence option.
* convert the date column into datetime. (exception: records with 3000-01-01 will be assigned to `call for availability`)
* create a month column from the date column. 



#### cleaning columns and handling types:

* change the type of `sq_feet`, `cats`, `dogs` , `baths`, and `beds` to int. (warning: some records in the `sq_feet` column are strings with descriptions of the space. These will be handled by the `clean_sq_feet_col` function, which will take out the digit based on the text it receives.)



#### Final steps

* remove duplicates if there are any.
* reset the index.


Should take action



* Create a prediction model with regression
* calculate statistics for seeing the dependency between variables.✅
* median and mean price per square feet for each type of residence.
* Desicion tree for calculating the importance of parameters.✅

Check at the end:
* Make sure all the columns are correctly assigned to their own type.
    * e.g., price, sq_feet should have int type
* Can I get whether a house is furnished/unfurnished?



Notes:


### Observations
* The only ones that can be explained based on sq_feet a bit, are condo, loft, and main floor.
