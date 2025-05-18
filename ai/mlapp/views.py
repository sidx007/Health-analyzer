from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import sys
import os

# Add the parent directory to sys.path to import the test module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the predict_diabetes function from test.py
from test import predict_diabetes

# Create your views here.
@ensure_csrf_cookie
def home(request):
    """
    View function for the home page of the site.
    """
    # Render the HTML template home.html
    return render(request, 'mlapp/home.html')

@ensure_csrf_cookie
def diabetes(request):
    """
    View function for the diabetes analysis page.
    """
    return render(request, 'mlapp/diabetes.html')

@ensure_csrf_cookie
def hypertension(request):
    """
    View function for the hypertension analysis page.
    """
    return render(request, 'mlapp/hypertension.html')

@ensure_csrf_cookie
def predict_diabetes_api(request):
    """
    API endpoint for diabetes prediction.
    """
    # Check for POST method
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method is allowed'}, status=405)
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Extract data from request with validation
        try:
            pregnancies = int(data.get('pregnancies', 0))
            glucose = float(data.get('glucose', 0))
            blood_pressure = float(data.get('bloodPressure', 0))
            skin_thickness = float(data.get('skinThickness', 0))
            insulin = float(data.get('insulin', 0))
            bmi = float(data.get('bmi', 0))
            diabetes_pedigree_function = float(data.get('diabetesPedigree', 0))
            age = int(data.get('age', 0))
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid data format: {str(e)}'
            }, status=400)
        
        # Make prediction
        try:
            prediction = predict_diabetes(
                pregnancies,
                glucose,
                blood_pressure,
                skin_thickness,
                insulin,
                bmi,
                diabetes_pedigree_function,
                age
            )
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Prediction error: {str(e)}'
            }, status=500)
          # Get prediction value (0 or 1)
        is_diabetic = bool(prediction[0])
        
        # Define classification based on prediction
        classification = "Diabetic" if is_diabetic else "Non-diabetic"
        
        # Return successful response with classification instead of percentage
        return JsonResponse({
            'success': True,
            'is_diabetic': is_diabetic,
            'classification': classification,
            'message': classification
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format in request body'
        }, status=400)
    except Exception as e:
        # Catch any unexpected errors
        import traceback
        error_info = traceback.format_exc()
        return JsonResponse({
            'success': False, 
            'error': f'Unexpected error: {str(e)}',
            'traceback': error_info
        }, status=500)

@ensure_csrf_cookie
def predict_hypertension_api(request):
    """
    API endpoint for hypertension prediction.
    """
    # Check for POST method
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method is allowed'}, status=405)
    
    try:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Extract data from request with validation
        try:
            age = int(data.get('age', 0))
            systolic = int(data.get('systolic', 0))
            diastolic = int(data.get('diastolic', 0))
            weight = float(data.get('weight', 0))
            height = float(data.get('height', 0))
            heart_rate = int(data.get('heartRate', 0))
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid data format: {str(e)}'
            }, status=400)
        
        # Calculate BMI
        bmi = weight / ((height/100) ** 2)
        
        # Here you would normally call a prediction model for hypertension
        # For now we'll use a simple placeholder logic
        # This is NOT medically accurate - just for demonstration
        hypertension_risk = False
        risk_percentage = 0
        
        if systolic > 140 or diastolic > 90:
            hypertension_risk = True
            # Calculate a risk percentage based on how much above normal values
            systolic_factor = max(0, (systolic - 120) / 80)  # 120 normal, 200 max
            diastolic_factor = max(0, (diastolic - 80) / 40)  # 80 normal, 120 max
            age_factor = min(1, max(0, (age - 40) / 40))  # Age risk increases after 40
            bmi_factor = max(0, (bmi - 25) / 15)  # BMI risk increases above 25
            
            risk_percentage = round((systolic_factor * 0.4 + diastolic_factor * 0.4 + age_factor * 0.1 + bmi_factor * 0.1) * 100)
        
        # Return successful response
        return JsonResponse({
            'success': True,
            'has_hypertension': hypertension_risk,
            'risk_percentage': risk_percentage,
            'message': 'Hypertension Risk' if hypertension_risk else 'Normal Blood Pressure',
            'systolic': systolic,
            'diastolic': diastolic
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format in request body'
        }, status=400)
    except Exception as e:
        # Catch any unexpected errors
        import traceback
        error_info = traceback.format_exc()
        return JsonResponse({
            'success': False, 
            'error': f'Unexpected error: {str(e)}',
            'traceback': error_info
        }, status=500)
