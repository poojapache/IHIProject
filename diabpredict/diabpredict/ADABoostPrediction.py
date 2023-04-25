import joblib
import sklearn
import numpy as np

class ADABoost():
    def __init__(self):
        self.model = joblib.load('adaboost_binary_model_nonscal.pkl')

    def age_to_value(self,age_str):
        age = int(age_str)
        if age >= 18 and age <= 24:
            return 1.0
        elif age >= 25 and age <= 29:
            return 2.0
        elif age >= 30 and age <= 34:
            return 3.0
        elif age >= 35 and age <= 39:
            return 4.0
        elif age >= 40 and age <= 44:
            return 5.0
        elif age >= 45 and age <= 49:
            return 6.0
        elif age >= 50 and age <= 54:
            return 7.0
        elif age >= 55 and age <= 59:
            return 8.0
        elif age >= 60 and age <= 64:
            return 9.0
        elif age >= 65 and age <= 69:
            return 10.0
        elif age >= 70 and age <= 74:
            return 11.0
        elif age >= 75 and age <= 79:
            return 12.0
        elif age >= 80:
            return 13.0
        else:
            return None

    def get_income_label(self,income):
        income = int(income)
        if income < 10000:
            return 1.0
        elif income < 15000:
            return 2.0
        elif income < 20000:
            return 3.0
        elif income < 25000:
            return 4.0
        elif income < 35000:
            return 5.0
        elif income < 50000:
            return 6.0
        elif income < 75000:
            return 7.0
        else:
            return 8.0

    def get_label_text(self, label):
            if label == 0:
                return "pre diabetes"
            elif label == 1:
                return "diabetes"
            # elif label == 2:
            #     return "diabetes"
            else:
                raise ValueError("Invalid prediction, try again: {}".format(label))

    def prediction(self,input_data):
                preprocessed_data = {
                "HighBP": float(input_data["HighBP"]),
                "HighChol": float(input_data["HighChol"]),
                "CholCheck": float(input_data["CholCheck"]),
                "BMI": float(input_data["BMI"]),
                "Smoker": float(input_data["Smoker"]),
                "Stroke": float(input_data["Stroke"]),
                "HeartDiseaseorAttack": float(input_data["HeartDiseaseorAttack"]),
                "PhysActivity": float(input_data["PhysActivity"]),
                "Fruits": float(input_data["Fruits"]),
                "Veggies": float(input_data["Veggies"]),
                "HvyAlcoholConsump": float(input_data["HvyAlcoholConsump"]),
                "AnyHealthcare": float(input_data["AnyHealthcare"]),
                "NoDocbcCost": float(input_data["NoDocbcCost"]),
                "GenHlth": float(input_data["GenHlth"]),
                "MentHlth": float(input_data["MentHlth"]),
                "PhysHlth": float(input_data["PhysHlth"]),
                "DiffWalk": float(input_data["DiffWalk"]),
                "Sex": 1.0 if input_data["Sex"].lower() == "m" else 0.0,  # assuming male=1, female=0
                "Age": self.age_to_value(input_data["Age"]),
                "Education": float(input_data["Education"]),
                "Income": self.get_income_label(float(input_data["Income"]))
                }

                # Convert the input data to a format that the model can use for prediction
                preprocessed_data = [[preprocessed_data[key] for key in preprocessed_data]]
                
                # Generate the prediction using the loaded model
                prediction = self.model.predict(preprocessed_data)[0]

                # Print the predicted value
                print(self.get_label_text(prediction))

                return prediction
