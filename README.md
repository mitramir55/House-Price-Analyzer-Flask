# House-price-prediction
![house](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.theatlantic.com%2Ffamily%2Farchive%2F2022%2F01%2Fwhen-good-time-buy-house%2F621409%2F&psig=AOvVaw1fUz9W7CeJzBkndeCgjFKu&ust=1649678896299000&source=images&cd=vfe&ved=0CAoQjRxqFwoTCMi9tPm6ifcCFQAAAAAdAAAAABAP)


Cities supported by RentFaster : [link](https://www.rentfaster.ca/cities/)

### Preprocessing

Should be removed
* replace undefined dates with call for ... ✅ 
* turn a to datetime ✅ 
* price null ✅ 
* square feet null ✅ 
* rented column ✅ 


Should take action
* create rows when neither sq_feet2 nor price2 are null. ✅ 
    * To be taken into new rows : bath2, sq_feet2, price2
    * To be copied: link, location
* Clean columns
    * baths ✅
    * beds ✅
* turn to int:
    * cats ✅
    * dogs ✅

* Create a regression plot showing square feet and price.✅
* A plot that outlines the price range in all communities✅
* automatic plotting against price for every column the user chooses.
* Create a prediction model with regression
* calculate statistics for seeing the dependency between variables.✅
* median and mean price per square feet for each type of residence.
* Desicion tree for calculating the importance of parameters.✅

Check at the end:
* Make sure all the columns are correctly assigned to their own type.
    * e.g., price, sq_feet should have int type
* Can I get whether a house is furnished/unfurnished?

Descriptions
Date:
dates that have 3000 in them, are "Call for availability"

### Observations
* The only ones that can be explained based on sq_feet a bit, are condo, loft, and main floor.