from django.shortcuts import render
import requests
import datetime

# Create your views here.

def home(request):

    url = "http://api.openweathermap.org/data/2.5/weather?q="
    apiKey = "a364ae9c6d6dbdf15bd73c5ed76c7cbd"
    nombreCiudad = request.GET.get('ciudad')

    if nombreCiudad is None:
        print(datetime.datetime.now())
        contexto = {
            "fecha": datetime.datetime.now(),
            'celsius':'NA',
            'pais':'---NA',
            'fahrenheit':'NA',
            'sensacion':'NA',
            'velocidad_viento':'NA',
            'clima':'NA',
            'presion':'NA',
            'humedad':'NA',
            'visibilidad':'NA'
        }
        print("regresa el index.html")
        return render(request, "index.html", contexto)

    else:
        print("Entra al else")
        print(url+nombreCiudad+'&appid='+apiKey)
        # peticion a la api
        response = requests.get(url+nombreCiudad+'&appid='+apiKey).json()
        if response['cod'] == 200:

            celcius = response['main']['temp'] - 273.15
            fahrenheit = celcius*9/5+32
            ciudad = response['name']
            pais = response['sys']['country']
            sensacion = response['main']['feels_like'] - 273.15
            velocidad_viento = response['wind']['speed']
            clima = response['weather'][0]['description']
            presion = response['main']['pressure']
            humedad = response['main']['humidity']
            visibilidad = response['visibility']
            icono = response['weather'][0]['icon']

            proximos_5_dias = "http://api.openweathermap.org/data/2.5/forecast?q="
            proximos_5_dias_response = requests.get(proximos_5_dias+nombreCiudad+'&mode=json'+'&appid='+apiKey).json()


            celcius_prox_5 = []
            fahrenheit_prox_5= []
            velocidad_viento_prox_5  = []
            clima_prox_5 = []
            presion_prox_5 = []
            humedad_prox_5 = []
            visibilidad_prox_5 = []
            fecha_prox_5 = []
            icono_prox_5 = []

            for i in range(0, 40):
                celcius_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['main']['temp_max'] - 273.15)
                fahrenheit_prox_5.append(celcius_prox_5[i]*9/5+32)
                velocidad_viento_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['wind']['speed'])
                clima_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['weather'][0]['main'])
                presion_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['main']['pressure'])
                humedad_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['main']['humidity'])
                visibilidad_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['visibility'])
                fecha_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['dt_txt'])
                icono_prox_5.append(proximos_5_dias_response['list'][i:i+1][0]['weather'][0]['icon'])
            
            data_prox_5 = list(zip(celcius_prox_5,fahrenheit_prox_5, velocidad_viento_prox_5, clima_prox_5, presion_prox_5, humedad_prox_5, visibilidad_prox_5, fecha_prox_5, icono_prox_5))
            contexto = {'fecha': datetime.datetime.now(),
                        'celcius':celcius,
                        'fahrenheit':fahrenheit,
                        'ciudad':ciudad,
                        'pais':pais,
                        'sensacion':sensacion,
                        'velocidad_viento':velocidad_viento,
                        'clima':clima,
                        'presion':presion,
                        'humedad':humedad,
                        'visibilidad':visibilidad,
                        'icono': icono,
                        'data_prox_5':data_prox_5,
                        }
            return render(request, "index.html", contexto)
        else:
            return render(request, 'error.html', {'titulo': 'Ciudad no encontrada'})

# 404: página no encontrada
def error404(request, exception):
    return render(request, "error.html", {'titulo': 'Página no encontrada'})