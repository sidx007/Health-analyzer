# prompt: make prefiction using the pickle file

import pickle
import pandas as pd
# Load the saved model
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

def predict_diabetes(
    pregnancies, 
    glucose, 
    blood_pressure, 
    skin_thickness, 
    insulin, 
    bmi, 
    diabetes_pedigree_function, 
    age
):
    obesity_1 = 1 if (bmi >= 30 and bmi < 35) else 0
    obesity_2 = 1 if (bmi >= 35 and bmi < 40) else 0
    obesity_3 = 1 if bmi >= 40 else 0
    overweight = 1 if (bmi >= 25 and bmi < 30) else 0
    underweight = 1 if bmi < 18.5 else 0
    
    # NewInsulinScore
    insulin_normal = 1 if (insulin >= 16 and insulin <= 166) else 0
    
    # NewGlucose categories
    glucose_low = 1 if glucose < 70 else 0
    glucose_normal = 1 if (glucose >= 70 and glucose < 100) else 0
    glucose_overweight = 1 if (glucose >= 100 and glucose < 126) else 0
    glucose_secret = 1 if glucose >= 126 else 0
    
    # Create input data DataFrame
    input_data = pd.DataFrame({
        'Pregnancies': [pregnancies],
        'Glucose': [glucose],
        'BloodPressure': [blood_pressure],
        'SkinThickness': [skin_thickness],
        'Insulin': [insulin],
        'BMI': [bmi],
        'DiabetesPedigreeFunction': [diabetes_pedigree_function],
        'Age': [age],
        'NewBMI_Obesity 1': [obesity_1],
        'NewBMI_Obesity 2': [obesity_2],
        'NewBMI_Obesity 3': [obesity_3],
        'NewBMI_Overweight': [overweight],
        'NewBMI_Underweight': [underweight],
        'NewInsulinScore_Normal': [insulin_normal],
        'NewGlucose_Low': [glucose_low],
        'NewGlucose_Normal': [glucose_normal],
        'NewGlucose_Overweight': [glucose_overweight],
        'NewGlucose_Secret': [glucose_secret]
    }, index=[0])
    
    # Make a prediction
    prediction = loaded_model.predict(input_data)
    
    return prediction

# Example usage
if __name__ == "__main__":
    # Example input parameters
    prediction = predict_diabetes(
        pregnancies=0,
        glucose=120.0,
        blood_pressure=70.0,
        skin_thickness=39.0,
        insulin=270.5,
        bmi=36.7,
        diabetes_pedigree_function=2.329,
        age=31
    )
    
    # Print the prediction
    print(f"Prediction: {prediction}")
    print(f"Diabetes Status: {'Diabetic' if prediction[0] == 1 else 'Non-diabetic'}")