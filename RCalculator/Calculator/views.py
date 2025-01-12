import json
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def calculator(request):
    return render(request, 'calculator.html')


@csrf_exempt  # Disable CSRF for the example. Enable CSRF handling in production.
def generate_json(request):
    if request.method == 'POST':
        # Get the request data
        data = json.loads(request.body)
        birth_date = data.get('birth_date')
        inflation_rate = float(data.get('inflation_rate', 0))

        # Create JSON response
        response_data = {
            'birth_date': birth_date,
            'inflation_rate': inflation_rate,
        }
        response_json = json.dumps(response_data, indent=4)

        # Send as a downloadable JSON file
        response = HttpResponse(response_json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="simulationData.json"'
        return response

    return JsonResponse({'error': 'Invalid method'}, status=400)


@csrf_exempt  # Disable CSRF for the example. Enable CSRF handling in production.
def generate_table(request):
    if request.method == 'POST':
        # Parse incoming JSON
        data = json.loads(request.body)
        birth_date_str = data.get('birth_date')
        inflation_rate = float(data.get('inflation_rate')) / 100

        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            current_date = datetime.now()
            days_since_birth = (current_date - birth_date).days
            years_since_birth = int(days_since_birth / 365.25)
            final_year = 110

            headers = ['Year', 'Age', 'XXX', 'YYY']
            fields = ['year', 'age', 'days_since_birth', 'calculated_value']

            # Generate the calculation results
            calculations = []
            for age in range(years_since_birth, final_year):
                year = birth_date.year + age
                days_in_year = (datetime(year, 12, 31) - datetime(year, 1, 1)).days
                calculated_value = days_in_year * 0.5  # Example calculation
                calculations.append({
                    "age": age,
                    "year": year,
                    "days_since_birth": days_since_birth,
                    "calculated_value": calculated_value,
                })

            # Return the calculations as a JSON response
            return JsonResponse({
                'headers': headers,
                'fields': fields,
                'rows': calculations})

        except ValueError as e:
            return JsonResponse({'error': f"Invalid date format: {str(e)}"}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
