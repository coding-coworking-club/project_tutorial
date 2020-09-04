# How convenient is it?
import convenienceEvaluation

# for place1
place1 = convenienceEvaluation.ConvenienceEvaluation(address = "台北市內湖區江南街41巷12號" , key = "AIzaSyCGqn72mnyMi1fG056z2cHvDRFt9wMkjKE")
place1.type_mapping(["food", "live", "transportation", "entertainment", "environment"])
place1.search(400)
place1.places_table.loc[:,["name", "distance", "vicinity", "rating", "latitude", "longitude"]]

place1.giving_weight()
place1.get_point()
# result 
place1.points
place1.total

# for place2
place2 = convenienceEvaluation.ConvenienceEvaluation(address = "台北市中正區羅斯福路四段一號" , key = "AIzaSyCGqn72mnyMi1fG056z2cHvDRFt9wMkjKE")
place2.type_mapping(["food", "live", "transportation", "entertainment", "environment"])
place2.search(400)
place2.giving_weight()
place2.get_point()
# result 
place2.points
place2.total